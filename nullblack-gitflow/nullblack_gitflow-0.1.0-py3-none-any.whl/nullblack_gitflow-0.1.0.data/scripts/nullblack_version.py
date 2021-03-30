#!python

import os
import sys
import subprocess
import time



default_env = os.environ.copy()


def run_exitcode(command, env=default_env, cwd=None, input_str="", get_output=False, show_output=True, silent=False):
    if show_output == None:
        show_output = not get_output

    with_out_msg = ""
    if get_output:
        with_out_msg = " Obtaining output"
    if not silent:
        print("Executing: (\"" + command + "\")" + ((" From " + cwd) if cwd else "") + with_out_msg, flush=True)
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, env=env, cwd=cwd)
    if (len(input_str) > 0):
        time.sleep(1)
        process.stdin.write(input_str)

    # Poll process for new output until finished

    output = ""
    nextline = ""
    while True:
        if get_output or show_output:
            nextline = process.stdout.readline()
        else:
            time.sleep(0.001)

        if process.poll() is not None:
            break

        if get_output:
            output += nextline
        if show_output:
            sys.stdout.write(nextline)
            sys.stdout.flush()

    if get_output:
        return process.returncode, output
    else:
        return process.returncode


def run(command, env = default_env, cwd = None, input_str="", get_output=False, show_output=None, silent=False):
    output = ""
    if get_output:
        exitCode, output = run_exitcode(command, env=env, cwd=cwd, input_str=input_str, get_output=True, show_output=show_output, silent=silent)
    else:
        exitCode = run_exitcode(command, env=env, cwd=cwd, input_str=input_str)


    if exitCode != 0:
        print('Command \'' + command + '\' failed!', flush=True)
        print('Expected error code 0, got ' + str(exitCode), flush=True)
        if get_output:
            print('output is:')
            print(output)
        os._exit(1)

    if get_output:
        return output



def parse_semver(version):
    if len(version) > 0 and version[0] == "v" and "." in version:
        #Release branch
        try:
            parts = version.split(".")
            version_major = int(parts[0][1:])#Skip the v
            version_minor = int(parts[1])

            if len(parts) == 4:
                #RC version IE x.y.z-rc.a
                version_patch = int(parts[2].replace("-rc", ""))
                version_rc = int(parts[3])
            else:
                version_patch = int(parts[2])
                version_rc = 0

            return (version_major, version_minor, version_patch, version_rc)

        except Exception as error:
            raise RuntimeError("Failed to parse: \"" + version + "\"") from error

    raise RuntimeError("\"" + version + "\" is not a valid semver version!")


def semver_to_number(tup):
    return (tup[0] << 24) | (tup[1] << 16) | (tup[2] << 8) | (tup[3] << 0)

def get_semver_tag_from_commit(commit):
    tags = run("git tag --points-at " + commit, get_output=True).splitlines()
    result = None
    for tag in tags:
        version = parse_semver(tag)
        if result == None or semver_to_number(version) > semver_to_number(result):
            print("Found good tag: " + str(version))
            result = version

    return result


def get_latest_parent_version(commit_hash="HEAD", max_depth=10, current_depth=0):
    if current_depth > 0:
        print("Recursed in get_latest_parent_version... depth={}, commit={}".format(current_depth, commit_hash))

    parents = run("git rev-parse \"" + commit_hash + "^@\"", get_output=True, show_output=True).splitlines()
    parent_version = None
    for parent in parents:
        try:
            parent_version = get_semver_tag_from_commit(parent)

        except:
            pass

    if parent_version == None:
        if current_depth == max_depth:
            print("Warning no parent commits are tagged after " + str(max_depth) + " tries. Was this commit merged from a commit that passed CI")
            return None
        else:
            for parent in parents:
                print("looping " + parent)
                #Recurse the parents of the parents until we find a good version or exceed the depth
                next_version = get_latest_parent_version(parent, max_depth, current_depth + 1)
                if parent_version == None or semver_to_number(next_version) > semver_to_number(parent_version):
                    parent_version = next_version

    return parent_version



def is_semver_unknown(semver):
    return semver[0] == 0 and semver[1] == 0 and semver[2] == 0 and semver[3] == 0

def is_semver_rc(semver):
    return semver[3] != 0

def semver_to_string(semver):
    if semver == None:
        return "None"

    major = semver[0]
    minor = semver[1]
    patch = semver[2]
    rc    = semver[3]

    if is_semver_unknown(semver):
        return "<unknown>"
    elif is_semver_rc(semver):
        return "v" + str(major) + "." + str(minor) + "." + str(patch) + "-rc." + str(rc)
    else:
        return "v" + str(major) + "." + str(minor) + "." + str(patch)

#Returns a list of commits "pushed" to a branch (excluding all merge commits from other parents
#along with their commit tree). This only includes commits between HEAD and the furthest point
#where this branch was merged into
#Useful for only looking at the commits "on a branch" for versioning purposes
def get_commits_on_current_branch(current_branch):
    result = []

    #Our strategy is to run git log origin/<BRANCH>..HEAD for all branches
    #and return the set of commits that in included in each branch's listing
    branches = list(filter(
        lambda branch: "origin/" in branch and not "HEAD" in branch,
        run("git branch -a", get_output=True).splitlines()))
    for i in range(0, len(branches)):
        branches[i] = branches[i].strip().replace("remotes/origin/", "")

    if len(branches) == 0:
        return []

    first_it = True
    for branch in branches:
        if branch == current_branch:
            continue

        current_hashes = []
        for line in run("git log origin/" + branch + "..HEAD --format=format:%H", get_output=True).splitlines():
            if first_it:
                result.append(line)
            else:
                current_hashes.append(line)

        if not first_it:
            next_result = []
            for hash in current_hashes:
                if hash in result:
                    next_result.append(hash)
            result = next_result
        first_it = False


    return result

#Takes a list of strings and returns a parsed tuple of the largest tuple or None if list contains no semver strings
def get_largest_semver(semver_list):
    largest = None
    for semver_str in semver_list:
        try:
            newest = parse_semver(semver_str)
            if largest == None or semver_to_number(newest) > semver_to_number(largest):
                largest = newest
        except:
            pass

    return largest


def versioned_branch(branch):
    return len(branch) > 0 and branch[0] == "v" and "." in branch or branch == "master" or branch == "hotfix"

#Returns a 4 element tuple of the version major, minor, patch, and RC (build). 
#Returns all zeros when the version could not be found
def get_next_version(disable_pull_tags=False):

    branch = run("git branch --show-current", get_output=True).strip()
    print("Branch is: \"" + branch + "\"")

    if not versioned_branch(branch):
        #Dont bother complex git checks if we are on develop or a feature branch
        if branch == "dev" or branch == "development" or "feature/" in branch:
            print("Currently on non-release branch")
        else:
            print("WARNING! Non-versined branch uses name that doesnt conform to null.black's gitflow standards!: \"" + branch + "\" see documentation: https://TODO")
        return (0, 0, 0, 0)

    local_changes = run("git diff-index HEAD", get_output=True)

    #Always try to pull tags before any tag related command if we are allowed to
    if not disable_pull_tags:
        run("git pull --tags")

    #If this commit was already tagged, return the tag version (usually some sort of CI or local rebuild)
    if len(local_changes) == 0:
        #And we have no local changes

        tags_on_current_commit = run("git tag --points-at HEAD", get_output=True).strip()
        if len(tags_on_current_commit) > 0:
            #This commit is already tagged
            lines = tags_on_current_commit.splitlines()
            if len(lines) > 1:
                print("Warning current commit is tagged more than once! Tags: " + str(lines))
                print("Picking first tag that is semver!")
                for tag in lines:
                    try:
                        result = parse_semver(tag)
                        print("Rebuilding tag: " + tag)
                        return result
                    except:
                        pass
            else:
                print("Rebuilding tag: " + tags_on_current_commit)
                return parse_semver(tags_on_current_commit)
    else:
        print("There are local changes so skipping check if the current commit is tagged")


    if len(branch) > 0 and branch[0] == "v" and "." in branch:
        #Release branch
        branch_semver = parse_semver(branch)
        print("Using {} as the base version since this is a release branch: ".format(semver_to_string(branch_semver)))

        #Find rc number
        #We need to find all tags that match with our branch version, and then pick rc.1 or increment the largest matching tag name

        largest = get_largest_semver(run("git tag --list \"" + branch + "*\"", get_output=True).splitlines())
        largest_str = semver_to_string(largest)

        print("got lagrest rc: " + largest_str)
        if largest != None:
            last_rc_hash = run("git rev-list -n 1 " + largest_str, get_output=True).strip()
            print("tag: " + largest_str + " is commit " + last_rc_hash)
            version_rc = largest[3] + 1
            print("Creating new rc #" + str(version_rc))

        else:
            #Start new RC's at 1
            version_rc = 1

        if branch_semver == None:
            return (0, 0, 0, 0)

        return (branch_semver[0], branch_semver[1], branch_semver[2], version_rc)


    elif branch == "master":
        print("Obtaining version from previous tagged commit on release branch or hotfix because this is master")
        #Master only ever contains merge commits from release branches and hotfix that have passed CI
        #Because release branches and hotfix commits that pass CI are tagged we are OK in assuming
        #The parent commit has a tag that we can use to determine the version
        parent_version = get_latest_parent_version()
        if parent_version == None:
            return (0, 0, 0, 0)
 
        #Version is the same as the parent commit but without the -rc.XXX
        return (parent_version[0], parent_version[1], parent_version[2], 0)

    elif branch == "hotfix":
        commits = get_commits_on_current_branch(branch)

        if len(commits) == 0:
            print("New merge onto hotfix. Obtaining version from previous tagged commit on master")
            #This is the first commit since a merge from other branches
            parent_version = get_latest_parent_version()

            if parent_version == None:
                return (0, 0, 0, 0)
            else:
                return (latest_version[0], latest_version[1], latest_version[2] + 1, 1)

        else:
            print("Using commit chain on hotfix to determine version")
            #Find the previous commit with the largest RC value and increment that once to find the new version
            latest_version = None
            for commit in commits:
                version = get_semver_tag_from_commit(commit)
                if version != None:
                    if latest_version == None or semver_to_number(version) > semver_to_number(latest_version):
                        latest_version = version

            print("latest version in hotfix chain: " + semver_to_string(latest_version))

            if latest_version != None:
                return (latest_version[0], latest_version[1], latest_version[2], latest_version[3] + 1)

            print("No tagged commits in chain: " + str(commits) + " looking for merge commit onto hotfix")
            latest_version = None
            for commit in commits:
                new_version = get_latest_parent_version(commit, 0, 1)
                if latest_version == None or semver_to_number(new_version) > semver_to_number(latest_version):
                    latest_version = new_version


            if latest_version != None:
                return (latest_version[0], latest_version[1], latest_version[2] + 1, 1)

            print("Warning! None of the commits: " + str(commits) + " (commits on hotfix) are tagged with a valid semver version!")
            print("Looking further back to find initial version to tag as...")

            if latest_version == None:
                print("FATAL! Failed to find version to base this hotfix version off of after reading parent commits from other branches")
            os._exit(1)


    else:
        raise RuntimeError("Unreachable")



def get_version_code():
    local_changes = run("git diff-index HEAD", get_output=True)
    base_count = int(run("git rev-list HEAD --count", get_output=True).strip())

    if len(local_changes) == 0:
        print("No local changes. Using the number of commits as the version code")
        return base_count
    else:
        print("Repo has uncommited changes. Counting an extra commit for the purposes of calculating the version code")
        return base_count + 1


if __name__ == "__main__":
    if "--test" in sys.argv:
        test()
        os._exit(1)

    version = get_next_version()
    string = semver_to_string(version)

    version_code = get_version_code()

    if is_semver_unknown(version):

        print("unknown version")

    elif is_semver_rc(version):
        print("Got PROD version: " + string + ", CODE: " + str(version_code))

    else:
        print("Got normal alpha version: " + string + ", CODE: " + str(version_code))



