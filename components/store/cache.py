import json
import csv
import pandas as pd
from pandas import DataFrame as df

class Cache(object):
    def __init__(self, filename):
        self.filename = filename

    # to store data to certain filename
    def store(self, obj):
        with open(self.filename, 'w') as file:
            file.write(json.dumps(obj))
            file.close()
        return True

    def update_csv(self, id, updated_data):
        baca = self.read_by_chunk()
        list_index = []
        data_iteration = 0
        for data in baca:
            idx = data[(data['CMGUnmaskedID'] == id)].index.tolist()
            list_index.append(idx)
            if len(idx) == 0:
                data_iteration += 10000
            elif len(idx) == 1:
                data_iteration += idx[0]
                break

        index_row = data_iteration+1
        print 'index rowww', index_row


        c = csv.writer(open(self.filename, 'r+'))
        qfile = file(self.filename, 'rb')
        csvreader = csv.reader(qfile)

        count = 0
        for x in csvreader:
            if count == index_row:
                c.writerow(updated_data)
            else:
                c.writerow(x)
            count += 1

        return updated_data, id

    def read(self, bottomlimit, toplimit):
        # set default value
        if (bottomlimit is None) and (toplimit is None):
            bottomlimit = 0
            toplimit = 100

        if bottomlimit == 0:
            skipstart = 0
        else:
            skipstart = 1

        read_csv = pd.read_csv(self.filename, skiprows=range(skipstart, bottomlimit), nrows=int(toplimit))
        return read_csv

    def header(self):
        reader = csv.reader(open(self.filename))
        header = reader.next()
        return header

    def filterbycategory(self, **kwargs):
        CMGUnmaskedID = kwargs.get('CMGUnmaskedID', None)
        ClientTier = kwargs.get('ClientTier', None)
        CMGSegmentName = kwargs.get('CMGSegmentName', None)
        GlobalControlPoint = kwargs.get('GlobalControlPoint', None)

        filter_result_in_chunk = []
        for data in self.read_by_chunk():
            if (CMGUnmaskedID != '') & (CMGUnmaskedID is not None):
                # print 'isi unmaskedID', CMGUnmaskedID
                filter_result_in_chunk.append(data[(data['CMGUnmaskedID'] == CMGUnmaskedID)])
            else:
                if (ClientTier!='') and (CMGSegmentName!='') and (GlobalControlPoint!='') :
                    filter_result_in_chunk.append(data[ (data['ClientTier'] == ClientTier) & (data['CMGSegmentName'] == CMGSegmentName) & (data['GlobalControlPoint'] == GlobalControlPoint) ] )
                elif (ClientTier!='') and (CMGSegmentName!='') :
                    filter_result_in_chunk.append(data[ (data['ClientTier'] == ClientTier) & (data['CMGSegmentName'] == CMGSegmentName) ] )
                elif (ClientTier!='') and (GlobalControlPoint!='') :
                    filter_result_in_chunk.append(data[ (data['ClientTier'] == ClientTier) & (data['GlobalControlPoint'] == GlobalControlPoint) ] )
                elif (CMGSegmentName!='') and (GlobalControlPoint!='') :
                    filter_result_in_chunk.append(data[ (data['CMGSegmentName'] == CMGSegmentName) & (data['GlobalControlPoint'] == GlobalControlPoint) ] )
                elif ClientTier!='':
                    filter_result_in_chunk.append(data[ (data['ClientTier'] == ClientTier) ] )
                elif CMGSegmentName!='':
                    filter_result_in_chunk.append(data[ (data['CMGSegmentName'] == CMGSegmentName) ] )
                elif GlobalControlPoint!='':
                    filter_result_in_chunk.append(data[ (data['GlobalControlPoint'] == GlobalControlPoint) ] )

        print filter_result_in_chunk
        filter_result = pd.concat(filter_result_in_chunk, ignore_index=True)
        return filter_result.to_dict(orient='record')

    # to load the whole data
    def read_by_chunk(self):
        return pd.read_csv(self.filename, chunksize=10000, iterator=True)

    def filterbynumber(self, **kwargs):
        filtered_data = kwargs.get('filtered_data', None)
        Type = kwargs.get('Type', None)
        Year = kwargs.get('Year', None)
        Start = kwargs.get('Start', None)
        End = kwargs.get('End', None)

        print 'parameter ', Year, Start, End
        data = pd.DataFrame(filtered_data)

        if Year == '2014' or Year == 2014:
            if Type == 'revenue':
                kolom = 'REVENUE_FY14'
            elif Type == 'deposits':
                kolom = ' Deposits_EOP_FY14'
        elif Year == '2015' or Year == 2015:
            if Type == 'revenue':
                kolom = 'REVENUE_FY15X'
            elif Type == 'deposits':
                kolom = ' Deposits_EOP_FY15x'

        data[kolom] = data[kolom].str.replace(',', '').convert_objects(convert_numeric=True)
        filter_range = data[(data[kolom] >= int(Start)) & (data[kolom] <= int(End))]

        return filter_range.to_dict(orient='record')


    # to load the data partly
    def loads(self, **kwargs):
        bottomlimit = kwargs.get('bottomlimit', None)
        toplimit = kwargs.get('toplimit', None)
        return self.read(bottomlimit,toplimit).to_dict(orient='record')

    def length_of_data(self):
        sum = 0
        length_chunk = []
        for x in self.read_by_chunk():
            length_chunk.append(len(x))

        for x in length_chunk:
            sum += x
        return sum

    def unique_list_in_column(self, **kwargs):
        if 'ClientTier' in kwargs:
            colum_name = kwargs.get('ClientTier')
        elif 'CMGSegmentName' in kwargs:
            colum_name = kwargs.get('CMGSegmentName')
        elif 'GlobalControlPoint' in kwargs:
            colum_name = kwargs.get('GlobalControlPoint')

        # CMGSegmentName = kwargs.get('CMGSegmentName', None)
        select_column = []
        uniq = []
        read_by_chunk = self.read_by_chunk()

        if colum_name is not None:
            for data in read_by_chunk:
                select_column.append( data[colum_name].tolist() )

            # to be fast
            for x in select_column[0]:
                if x not in uniq:
                    uniq.append(x)
        return uniq

    def is_empty(self):
        return self.length_of_data == 0