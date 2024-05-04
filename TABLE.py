    
class Table:
    def __init__(self):
        self.table={}

        

    def add_rsu_routing_table(self,rsu):
        rsu_tpl=(rsu['host'],rsu['port'],rsu['x'],rsu['y'])
        self.table[str(rsu['id'])]=rsu_tpl
        return self.table

    def update_rsu_routing(self,rsu):
        self.table[str(rsu.id)]=(rsu.host,rsu.port,rsu.x,rsu.y)
    
    def get_port(self,id):
        print(id)
        return self.table[id][1]



table_instance=Table()


