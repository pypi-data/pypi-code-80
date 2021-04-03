#!/usr/bin/env python

def as_sts_cmd(role_arn, mfa_arn, session_name='whaaa'):
    token_code = input(f"Enter you AWS MFA TOKEN: ")

    a = 'aws sts assume-role \\\n' \
        f'--role-arn {role_arn} \\\n' \
        f'--role-session-name {session_name} \\\n' \
        f'--serial-number {mfa_arn} \\\n' \
        f'--token-code {token_code}'

    return a


if __name__ == "__main__":

    a = as_sts_cmd(
        role_arn='arn:aws:iam::726797183957:role/eks_dev',
        mfa_arn='arn:aws:iam::726797183957:mfa/eks_role_assume_gid',
        session_name='eks_dev'
    )

    print(a)

