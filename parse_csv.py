import csv

with open('products_export_1.csv','r', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file)
    with open('updated_products_list.csv','w', encoding="utf8") as new_file:
        csv_writer = csv.writer(new_file)
        # next(csv_reader)
        for line in csv_reader:
            csv_writer.writerow(line)