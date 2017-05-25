from flask import Blueprint, jsonify, request, render_template, redirect, url_for

def wrapApiConvUser(compRepo):
    ApiConvUser = Blueprint('ApiConvUser', __name__)

    # REST interface to be implemented
    @ApiConvUser.route('/companydetailupdate/<string:id>', methods=['POST'])
    def update_companydetail(id):
        new_revenue_14 = request.form.get('new_revenue_14')
        new_revenue_15 = request.form.get('new_revenue_15')
        update = compRepo.update_detail(id, new_revenue_14, new_revenue_15)
        return redirect(url_for('ApiConvUser.get_companydetail', id=id))
        # return redirect(url_for('ApiConvUser.update_companydetail', id=id))

    @ApiConvUser.route('/companydetail/<string:id>', methods=['GET'])
    def get_companydetail(id):
        result = compRepo.get(id)
        column_name = compRepo.get_header()

        new_revenue_14 = request.form.get('new_revenue_14')
        new_revenue_15 = request.form.get('new_revenue_15')

        return render_template('company_detail.html', company_detail=result[0], list_column_name=column_name, updated_revenue=[new_revenue_14, new_revenue_15])

    @ApiConvUser.route('/companylists/', methods=['GET'])
    def get_companylists():
        page = request.args.get('page', None)
        limitperpage = request.args.get('limit', None)
        ClientTier = request.args.get('client_tier', None)
        CMGSegmentName = request.args.get('cmg_segment_name', None)
        GlobalControlPoint = request.args.get('global_control_point', None)

        year = request.args.get('year', None)
        revenue_start = request.args.get('revenue_start', None)
        revenue_end = request.args.get('revenue_end', None)
        deposits_start = request.args.get('deposits_start', None)
        deposits_end = request.args.get('deposits_end', None)
        roe_start = request.args.get('roe_start', None)
        roe_end = request.args.get('roe_end', None)


        if (page is None) or (limitperpage is None):
            page = 1
            limitperpage = 100

        # if not page.isdigit() and not limitperpage.isdigit():
        #    abort(404)

        if ClientTier is not None:
            result, numOfpages = compRepo.filter(ClientTier=ClientTier, CMGSegmentName=CMGSegmentName, GlobalControlPoint=GlobalControlPoint,
                                                 Year=year, RevenueStart=revenue_start, RevenueEnd=revenue_end,
                                                 DepositsStart=deposits_start, DepositsEnd=deposits_end)
        else:
            result, numOfpages = compRepo.list(int(page), int(limitperpage))
        return render_template('company_list.html',
                               company_list=result, limitperpage = int(limitperpage), numOfpages=numOfpages,
                               client_tier_options = compRepo.option_ClientTier(),
                               global_control_point_options = compRepo.option_GlobalControlPoint(),
                               cmg_segment_name_options = compRepo.option_CMGSegmentName(),
                               selected_client_tier = ClientTier,
                               selected_cmg_segment_name = CMGSegmentName,
                               selected_global_control_point = GlobalControlPoint,
                               selected_year = year,
                               selected_revenue_start = revenue_start,
                               selected_revenue_end = revenue_end,
                               selected_deposits_start = deposits_start,
                               selected_deposits_end = deposits_end,
                               selected_roe_start = roe_start,
                               selected_roe_end = roe_end
                               )

    @ApiConvUser.route('/options/', methods=['GET'])
    def get_options():
        option = compRepo.option_ClientTier()
        option1 = compRepo.option_CMGSegmentName()
        option2 = compRepo.option_GlobalControlPoint()
        header = compRepo.get_header()
        range_revenue = compRepo.show_range('2015', '3000000' , '4000000')
        return jsonify({'range':range_revenue, 'header':header, 'data':option, 'data1':option1, 'data2':option2})

    @ApiConvUser.route('/companycount/', methods=['GET'])
    def get_companycount():
        companycount = compRepo.total_rows()
        return jsonify({'data':companycount})

    @ApiConvUser.route('/')
    def main():
        return redirect(url_for('ApiConvUser.get_companylists'))

    return(ApiConvUser)