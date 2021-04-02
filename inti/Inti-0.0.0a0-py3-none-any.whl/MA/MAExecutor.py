
import psutil
from joblib import Parallel, delayed
import multiprocessing as mp

ma_obj = None


def process_wrapper(file_name, collection_name, chunkStart, chunkSize):
    """
    wrapper to execute the function outside on the class,
    this trick is required for the module multiprocessing
    to avoid serialization problems
    """
    global ma_obj
    return ma_obj.process_wrapper(
        file_name, collection_name, chunkStart, chunkSize)


def MAExecutorJL(obj, file_name, collection_name, max_threads=None):
    """
    Function to call the parallel insertion of data by chunks
    using multiprocessing module.
    Keyword arguments:
    obj -- Object from class MABase
    max_threads -- total number processors to use in parallel
    """
    if max_threads is None:
        jobs = psutil.cpu_count()
    else:
        jobs = max_threads

    Parallel(
        n_jobs=jobs,
        backend="multiprocessing",
        verbose=0)(
        delayed(
            obj.process_wrapper)(
                file_name,
                collection_name,
                chunkStart,
                chunkSize) for chunkStart,
        chunkSize in obj.chunkify(file_name))


def MAExecutorMP(obj, file_name, collection_name, max_threads=None):
    """
    Function to call the parallel insertion of data by chunks
    using multiprocessing module.
    Keyword arguments:
    obj -- Object from class MABase
    max_threads -- total number processors to use in parallel
    """
    global ma_obj
    ma_obj = obj
    if max_threads is None:
        jobs = psutil.cpu_count()
    else:
        jobs = max_threads

    pool = mp.Pool(max_threads)
    jobs = []

    # create jobs
    counter = 0
    for chunkStart, chunkSize in obj.chunkify(file_name):
        jobs.append(
            pool.apply_async(
                process_wrapper, [
                    file_name, collection_name, chunkStart, chunkSize]))
        counter = counter + 1

    # wait for all jobs to finish
    for job in jobs:
        job.get()

    # clean up
    pool.close()
    return True


def MAExecutor(obj, file_name, collection_name, max_threads=None, joblib=True):
    if joblib:
        MAExecutorJL(obj, file_name, collection_name, max_threads)
    else:  # Native multiprocessing
        MAExecutorMP(obj, file_name, collection_name, max_threads)
