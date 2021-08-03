from datetime import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import psycopg2

class BMS_RSGM(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()

    def set_content(self, content):
        self.content = content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print(request.payload.decode("utf-8"))
        conn = psycopg2.connect("dbname=AMC user=postgres password=nakerinaja")
        pl = request.payload.decode('utf-8').split("|")
        sql = 'INSERT INTO "public"."Realtime_Data" ("id_node","waktu_akuisisi","wa_integer","waktu_server","ws_integer","iluminansi","temperatur","kelembapan","panjang_pesan") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cur = conn.cursor()
        nid = pl[0]
        rd = pl[1].split("-")
        ld = pl[2]
        ts = str(datetime.now())
        tsi = datetime.now().timestamp()
        ta = datetime.fromtimestamp(float(rd[0]))
        tai = rd[0]
        data = (nid,ta,tai,ts,tsi,rd[3],rd[1],rd[2],ld)
        cur.execute(sql, data)
        conn.commit()
        conn.close()
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['BMS_RSGM'], BMS_RSGM())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()