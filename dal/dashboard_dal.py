from dal.db import call_proc

def istatistik():
    r = call_proc('sp_DashboardIstatistik'); return r[0] if r else {}
