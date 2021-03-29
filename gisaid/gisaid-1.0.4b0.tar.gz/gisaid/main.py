from gisaid.helpers import *
from gisaid.auth import *
from gisaid.exceptions import *
import time


class GiSaid(object):
    """
    Class for uploading & downloading to & from GISAID.
    Provides a route for automation or back-end integration.

    Parameters
    ----------
    args:
        csv_path, fasta_path or authentication info


    Returns
    ----------
    response:
        output from request


    Examples
    ----------
    >>> import gisaid as gs
    >>> gs.GiSaid(authenticate=True, client_id=client_id,
    >>>           username=username, password=password, filename=filename)
    Authentication successful
    """

    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.kwargs = None
            self.args = args
            self.data = read_files(self.args)
            self.__authf = authfile()
        elif kwargs["authenticate"]:
            self.kwargs = kwargs
            self.args = None
            self.data = authenticate(self.kwargs)
        elif kwargs["collate_fasta"]:
            self.kwargs = kwargs
            self.args = args
            self.data = collate_fa(self)
        else:
            raise InputError

    def upload(self):
        """
        Upload to GISAID

        Parameters
        ----------
        self:
            csv_path, fasta_path, jsoncred_path


        Returns
        ----------
        response:
            output from request


        Examples
        ----------
        >>> import gisaid as gs
        >>> x = gs.GiSaid(csv_file, fasta_file)
        >>> gs.upload()
        Upload successful
        """

        s = requests.Session()
        urls = "https://gpsapi.epicov.org/epi3/gps_api"
        resp1 = s.post(
            url=urls,
            json={
                "cmd": "state/session/logon",
                "api": {"version": 1},
                "ctx": "CoV",
                "client_id": self.__authf["client_id"],
                "auth_token": self.__authf["client_token"]
            }
        )

        time.sleep(0.01)
        try:
            resp2 = [
                logfile(
                    x["covv_virus_name"],
                    s.post(
                        url=urls,
                        json={
                            "cmd": "data/hcov-19/upload",
                            "sid": resp1.json()["sid"],
                            "data": x,
                            "submitter": x["submitter"],
                        },

                    ).json(),
                )
                for x in self.data
            ]
        except TypeError:
            raise DataError

        s.post(url=urls, json={"cmd": "state/session/logoff"})
        count = 0
        bad = 0
        with open("logfile.csv") as f:
            for line in f:
                if "success" in line:
                    count += 1
                else:
                    bad += 1
        print(f"{bad} failed uploads")
        print(f"{count} successful uploads")
        
        
    def upload_sql(self, db_name, if_exists, conn):
        """
        Insert record to SQL database

        Parameters
        ----------
        self:
            data
            
        db_name:
            SQL table name
    
        if_exists:
            replace or append
            
        Returns
        ----------
        response:
            None


        Examples
        ----------
        >>> import gisaid as gs
        >>> x = gs.GiSaid(csv_file, fasta_file)
        >>> x.upload_sql('foobar', 'append', conn)
        
        """
        record = pd.DataFrame.from_records(self.data)
        record.to_sql(db_name, conn, if_exists=if_exists)


    def download(self):
        """add gisaid api data interactions"""
        ...
    