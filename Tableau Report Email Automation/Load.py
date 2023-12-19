from config import *
import tableauserverclient as TSC
from configuration import *
import logging
from datetime import datetime, date

def Tableau_report():
    logging.info('Making connection with Tableau.')
    tableau_auth = TSC.TableauAuth(tableau_user, tableau_passwd)
    server = TSC.Server(tableau_server)
    server.version = tableau_version

    Email_Setting={ k:v for k,v in sect_dict.items()}

    #print(Email_Setting)

    with server.auth.sign_in(tableau_auth):
        for wb in TSC.Pager(server.workbooks):
            if wb.name in 'MT FT Report 1.0':
                workbook=server.workbooks.get_by_id(wb.id)
                logging.info(workbook.name)
                server.workbooks.populate_views(workbook)
                all_views=[view for view in workbook.views]
                pdf_req_option = TSC.PDFRequestOptions(
                                page_type=TSC.PDFRequestOptions.PageType.A4, 
                                orientation=TSC.PDFRequestOptions.Orientation.Landscape)
                image_req_option = TSC.ImageRequestOptions(imageresolution=TSC.ImageRequestOptions.Resolution.High, maxage=1)

                for view in all_views:
                    if view.name in Email_Setting['Financial Transaction']['reports_name']:
                        print(view)

                        filter_year = Email_Setting['Financial Transaction']['filter_year']
                        filter_month = Email_Setting['Financial Transaction']['filter_month']
                        month = datetime.now().strftime("%m")  # "January"
                        year = datetime.now().strftime("%Y")
                        # month = 'September'
                        filter_spn = Email_Setting['Financial Transaction']['filter_spn']
                        filter_spn_value = Email_Setting['Financial Transaction']['filter_spn_value']

                        pdf_req_option.vf(filter_year, year)
                        pdf_req_option.vf(filter_month, month)
                        #pdf_req_option.vf(filter_spn, filter_spn_value)

                        image_req_option.vf(filter_year, year)
                        image_req_option.vf(filter_month, month)
                        #image_req_option.vf(filter_spn, filter_spn_value)
                        print(image_req_option.view_filters)

                        server.views.populate_pdf(view, pdf_req_option) 
                        server.views.populate_image(view,image_req_option)
                        #server.views.populate_filter(view, filter_month, 'July')

                        # images_path=[ Email_Setting['Financial Transaction']['image_path']+"/"+i for i in os.listdir(Email_Setting['Financial Transaction']['image_path']) ]
                        # pdfs_path=[ Email_Setting['Financial Transaction']['pdf_path']+"/"+i for i in os.listdir(Email_Setting['Financial Transaction']['pdf_path']) ]

                        logging.info('Downloading Image.')

                        with open('{}/{}.{}'.format(Email_Setting['Financial Transaction']['image_path'],view.name,Email_Setting['Financial Transaction']['file_format'].split(",")[1]),'wb') as f: 
                            f.write(view.image)
                            image_path = f.name

                        logging.info(f'Downloading PDF.')
                        with open('{}/{}.{}'.format(Email_Setting['Financial Transaction']['pdf_path'],view.name,Email_Setting['Financial Transaction']['file_format'].split(",")[0]),'wb') as f:
                            f.write(view.pdf)
                            pdf_path = f.name

                        logging.info(f'Image Downloaded in path: {image_path}.')
                        logging.info(f'PDF Downloaded in path: {pdf_path}.')


    return image_path, pdf_path