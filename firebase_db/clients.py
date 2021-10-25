from firebase_admin import db,firestore
from datetime import datetime
class Data:
    
    def __init__(self, doc_id:str, dict_data:dict) -> None:
        for key in dict_data:
            setattr(self,key,dict_data[key])
        setattr(self,'id',doc_id)
        self.full_name = f'{self.firstname} {self.lastname}'
        
        cate_dict = {'1': 'A', '50': 'K', '2': 'B', '3': 'C', '23': 'C1'}
        try:
            category = cate_dict[str(self.cate)]
            setattr(self,'category',category)
        except:
            setattr(self,'category',str(self.cate))

        
    def __str__(self):
        return self.full_name
    
    @property
    def displayBG(self):
        d={'1':'A+','2':'B+','3':'AB+','4':'O+','5':'A-','6':'B-','7':'AB-','8':'O-'}
        try:
            return d[str(self.bloodgroup)]
        except :
            return self.bloodgroup

    def update(self,**kwargs):
        clients = Client()
        clients.clients_ref.document(self.id).update(kwargs)


class Client:
    def __init__(self):
        db = firestore.client()
        self.clients_ref = db.collection(u'client')
        
    def getNClients(self, limit=40, last_doc_clientAddedAt=None,staff=None,query=None):
        if query is None:
            query = self.clients_ref
        if staff:
            query = (
                query
                .where(u'staff',u'==',staff)
            )
            
            
        if last_doc_clientAddedAt is None:            
            query = ( 
                query
                .order_by(
                    u'clientAddedAt', 
                    direction=firestore.Query.DESCENDING
                )
                .limit(limit)
            )
            
        else:
            client_added_date = last_doc_clientAddedAt
            query = (
                query
                .order_by(
                    u'clientAddedAt', 
                    direction=firestore.Query.DESCENDING
                )
                .start_after({
                    u'clientAddedAt':client_added_date
                })
                .limit(limit)
            )
        docs = query.get()
        doc_list = list(docs)
        if len(doc_list) == 0:
            return [],last_doc_clientAddedAt
        else:
            last_doc_clientAddedAt = list(docs)[-1].to_dict()[u'clientAddedAt']        
            return [Data(doc.id,doc.to_dict()) for doc in docs],last_doc_clientAddedAt
    
    def get_by_id(self, id):
        doc = self.clients_ref.document(id).get()
        return Data(doc.id,doc.to_dict())
    
    
    def page_filter(self,_dict):
        keys=[key_ for key_ in _dict]
        def dateRef(action):
            docs=self.clients_ref.where(action, u'>=', _dict[action]).stream()
            return [Data(doc.id,doc.to_dict()) for doc in docs]

        query_ref=self.clients_ref
        c_flag=False
        date_flag=False
        for key in _dict:
            if not (key=='clientAddedAt' or key=='clientSubmittedAt' or key=='entry_users'):
                query_ref=query_ref.where(key,u'==',_dict[key])

            if key=="entry_users":
                query_ref=query_ref.where(u'entry_users',u'array_contains_any',[u'all_users',_dict[key]])
            docs = query_ref.stream()
            client_objects = [Data(doc.id,doc.to_dict()) for doc in docs]
            c_flag=True



        if 'clientAddedAt' in keys or 'clientSubmittedAt' in keys:
            if 'clientAddedAt' in keys and 'clientSubmittedAt' not in keys:
                client_objects2 = dateRef('clientAddedAt')
            elif 'clientAddedAt' not in keys and 'clientSubmittedAt' in keys:
                client_objects2 = dateRef('clientSubmittedAt')
            else:
                c1 = dateRef('clientAddedAt')
                c2 = dateRef('clientSubmittedAt')
                client_objects2 = list(filter(lambda c: c.id in [e.id for e in c2], c1))

            date_flag=True

        if c_flag and date_flag:
            client_objects = list(filter(lambda c: c.id in [e.id for e in client_objects2], client_objects))
        if date_flag and not c_flag:
            return client_objects2

        return client_objects
    
    def add(self,doc_id,**kwargs):
        self.clients_ref.document(doc_id).set(kwargs)
    
    def delete(self,id):
        self.clients_ref.document(id).delete()
    
    def update(self,id,**kwargs):
        self.clients_ref.document(id).update(kwargs)
        return self.get_by_id(id)    
    
    def search(self,value,staff=None):
        value = value.strip().title()
        if value.isnumeric():
            query = self.clients_ref.where(u'mobileNumber',u'==',value)
        else:                
            v_list = value.split()
            query = self.clients_ref.where(u'firstname',u'==',v_list[0])
            if len(v_list)>1:
                for v in v_list[1:]:
                    query = query.where(u'lastname',u'==',v)
        if staff:
            query = query.where(u'staff',u'==',staff)
        docs = query.stream()
        
        return [Data(doc.id,doc.to_dict()) for doc in docs]
    
    def filter_for_index(self,**kwargs):
        query = self.clients_ref
        for key in kwargs:            
                query = query.where(key,u'==',kwargs[key])
        query = query.order_by(u'clientAddedAt',direction=firestore.Query.ASCENDING)    
        docs = query.stream()
        return [Data(doc.id,doc.to_dict()) for doc in docs]
    
    def filter(self,**kwargs):
        query = self.clients_ref
        for key in kwargs:            
            query = query.where(key,u'==',kwargs[key])
        docs = query.stream()
        return [Data(doc.id,doc.to_dict()) for doc in docs]
        
if __name__ == '__main__':
    from datetime import datetime
    from initialize import initialize_firebase
    initialize_firebase()
    client = Client()
    clients = client.filter(staff='Sudip_panthi')
    for c in clients:
        c.update(staff='sudip_panthi')
        print('updated')
    
    
    
    