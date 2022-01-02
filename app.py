from flask import Flask, jsonify, request
import bs4
import csv
import re

from flask.json import tag

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return "Flask App Running"

@app.route('/parseCSV', methods=['GET'])
def parseCSV():
    with open('products_export_1.csv','r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        with open('updated_products_list.csv','w', encoding="utf8") as new_file:
            csv_writer = csv.writer(new_file, delimiter=',')
            # next(csv_reader)
            for line in csv_reader:
                csv_writer.writerow(line)
    return "CSV parsed successfully!"

@app.route('/csvReader', methods=['GET'])
def csvReader():
    with open('updated_products_list.csv','r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            print(line['Handle'])
    return "CSV read successfully!"
    

@app.route('/updateProductList', methods=['POST'])
def updateProductList():
    with open('products_export_1.csv','r', encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file)
        fields = next(reader)
        with open("new_products_list.csv", "w", encoding="utf8") as csv_write_file:
            writer = csv.DictWriter(csv_write_file, fieldnames=fields, delimiter=',')
            writer.writeheader()
            for row in reader:
                row[request.json['column_name']] = request.json['column_value']
                writer.writerow(row)
    return jsonify({'status' : "Success", 'status_code' : 200, 'message' : "CSV updated successfully!"})


@app.route('/updateProductListHTML', methods=['POST'])
def updateProductListHTML():
    with open('products_export_1.csv','r', encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file)
        fields = next(reader)
        with open("new_products_list.csv", "w", encoding="utf8") as csv_write_file:
            writer = csv.DictWriter(csv_write_file, fieldnames=fields)
            writer.writeheader()
        #     # next(csv_reader)
        #     for line in reader:
        #         csv_writer.writerow(line)
            for row in reader:
                doc = bs4.BeautifulSoup(row['Body (HTML)'], "html.parser")
                # print(doc.prettify)
                tags = doc.find(text="Dimension (D x H): ")
                # span = doc.find('span' ,attrs={'color':'#a59548;'})
                # tags = doc.find_all(["span"], recursive=True)
                # tags = doc.find_all(text=re.compile("\:.*"))
                # print(tags)
                if tags is not None:
                    level2Parent = tags.parent.parent
                    level2Parent.next_sibling = '<span style="color: #000000;">777mm x 777mm</span>'
                    # print(tags.parent.parent.next_sibling)
                    print(doc)
                    row['Body (HTML)'] = doc
                writer.writerow(row)
    return jsonify({'status' : "Success", 'status_code' : 200, 'message' : "CSV updated successfully!"})

if __name__ == "__main__":
    app.run('127.0.0.1', port=5500, debug=True)