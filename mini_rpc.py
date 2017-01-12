import xmlrpc
import xmlrpc.client

conf={
    'dbname': 'starter',
    'host': 'localhost',
    'port': 9999,
}

class RPC_Proxy():
    def __init__(self,dbname,host,port=80):
        self.dbname=dbname
        url="http://%s:%d/xmlrpc"%(host,port)
        self.proxy=xmlrpc.client.ServerProxy(url,allow_none=True)

    def login(self,login,password):
        data={
            "db_name": self.dbname,
            "login": login,
            "password": password,
        }
        ctx={
            "data": data,
        }
        try:
            res=self.proxy.execute("login","login",[],{"context":ctx})
        except xmlrpc.client.Fault as e:
            raise Exception("Remote error: %s"%e.faultString)
        cookies=res["cookies"]
        self.remote_user_id=cookies["user_id"]
        self.remote_token=cookies["token"]

    def execute(self,model,method,args,opts={}):
        #print("RPC_Proxy.execute",model,method,args,opts)
        if not self.remote_user_id or not self.remote_token:
            raise Exception("Need to login first")
        try:
            res=self.proxy.execute(model,method,args,opts,self.dbname,self.remote_user_id,self.remote_token)
        except xmlrpc.client.Fault as e:
            raise Exception("Remote error: %s"%e.faultString)
        return res

def connect_erp(login='admin', password='1234'):
    con=RPC_Proxy(conf['dbname'], conf['host'], conf['port'])
    con.login(login,password)
    if not con:
        raise Exception("Can not connect erp")
    return con


erp=connect_erp()
args=[[]]
sales=erp.execute('sale.order','search',(args))

print(sales)

