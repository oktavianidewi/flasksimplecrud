class Repo(object):
    def __init__(self, mem_store):
        self.cache = mem_store

    def response_message(self, response, data):
        return {'data': data, 'response':response}

    def create(self, data):
        try:
            insert = self.cache.store(data)
            result = self.response_message(True, data)
        except:
            result = self.response_message(False, 'Fail to store data.')
        return result
        # return self.cache.store(data)

    def get_all(self):
        try:
            data = self.cache.loads()
            result = self.response_message(True, data)
        except self.cache.is_empty():
            result = self.response_message(False, 'No data found.')
        return result

    def get_header(self):
        return self.cache.header()

    def get(self, id):
        findbyid = self.cache.filterbycategory(CMGUnmaskedID=id)
        if findbyid:
            result = self.response_message(True, findbyid)
        else:
            result = self.response_message(False, 'ID is not found')
        return findbyid
        # return

    def filter(self, **kwargs):
        ClientTier = kwargs.get('ClientTier', None)
        CMGSegmentName = kwargs.get('CMGSegmentName', None)
        GlobalControlPoint = kwargs.get('GlobalControlPoint', None)

        Year = kwargs.get('Year', None)
        RevenueStart = kwargs.get('RevenueStart', None)
        RevenueEnd = kwargs.get('RevenueEnd', None)
        DepositsStart = kwargs.get('DepositsStart', None)
        DepositsEnd = kwargs.get('DepositsEnd', None)

        filter = self.cache.filterbycategory(ClientTier=ClientTier, CMGSegmentName=CMGSegmentName, GlobalControlPoint=GlobalControlPoint)
        if (Year != '') and (DepositsStart != '') and (DepositsEnd != '') and (RevenueStart != '') and (RevenueEnd != ''):
            result1 = self.cache.filterbynumber(filtered_data=filter, Type='revenue', Year=Year, Start=RevenueStart, End=RevenueEnd)
            result = self.cache.filterbynumber(filtered_data=result1, Type='deposits', Year=Year, Start = DepositsStart, End = DepositsEnd)
        elif (Year != '') and (RevenueStart != '') and (RevenueEnd != ''):
            result = self.cache.filterbynumber(filtered_data = filter, Type='revenue', Year=Year, Start=RevenueStart, End=RevenueEnd)
        elif (Year != '') and (DepositsStart != '') and (DepositsEnd != ''):
            result = self.cache.filterbynumber(filtered_data = filter, Type='deposits', Year=Year, Start=DepositsStart, End=DepositsEnd)
        else:
            result = filter

        return result, 10

    def list(self, page, limitperpage):
        length_data = self.cache.length_of_data()
        if length_data > 0 :
            load_data = self.cache.loads(bottomlimit=(page-1)*limitperpage, toplimit=page*limitperpage)
            result = load_data, length_data
        else:
            result = self.response_message(False, 'Empty memory')
        return result

    def show_range(self, Year, Start, End):
        hasil = self.cache.range(Year, Start, End)
        print hasil
        return hasil

    def option_GlobalControlPoint(self):
        result = self.cache.unique_list_in_column(GlobalControlPoint='GlobalControlPoint')
        return result

    def option_CMGSegmentName(self):
        result = self.cache.unique_list_in_column(CMGSegmentName='CMGSegmentName')
        return result

    def option_ClientTier(self):
        result = self.cache.unique_list_in_column(ClientTier='ClientTier')
        return result

    def total_rows(self):
        return self.cache.length_of_data()

    def update_detail(self, id, revenue14, revenue15):
        # gabungkan dengan data lengkap
        updated_data = self.get(id)[0]
        updated_data['REVENUE_FY14'] = revenue14
        updated_data['REVENUE_FY15X'] = revenue15

        list_updated_data = []
        for i in self.get_header():
            list_updated_data.append(updated_data[i])

        result = self.cache.update_csv(id, list_updated_data)
        return result

    def remove(self, id):
        get_id = self.get(id)

        if get_id['response']:
            delete = self.cache.pop(id)
            result = self.response_message(True, delete)
        else:
            result = self.response_message(False, 'Error')
        return result