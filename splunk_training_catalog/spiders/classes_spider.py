import scrapy
""" 
Fundamentals 1 - On Demand
Fundamentals 2 - On Demand

Splunk Enterprise System Admin - 'https://education.splunk.com/instructor-led-training/splunk-enterprise-80-system-administration'
Splunk Enterprise Data Administration - 'https://education.splunk.com/instructor-led-training/splunk-enterprise-80-data-administration'

Architecting Splunk Enterprise Deployments - 'https://education.splunk.com/instructor-led-training/architecting-splunk-801-enterprise-deployments',
Troubleshooting Splunk Enterprise - https://education.splunk.com/instructor-led-training/troubleshooting-splunk-enterprise-80
Splunk Enterprise Cluster Administration - https://education.splunk.com/instructor-led-training/splunk-801-cluster-administration
Splunk Deployment Practical Lab - https://education.splunk.com/instructor-led-training/splunk-enterprise-deployment-practical-lab

Fundamentals 3 - On Demand
Creating Dashboards with Splunk - On Demand - https://education.splunk.com/instructor-led-training/creating-dashboards-with-splunk-80
Advanced Searching and Reporting - 'https://education.splunk.com/instructor-led-training/advanced-searching-and-reporting-with-splunk-80'
ILT Services Core Implementation Course -https://education.splunk.com/instructor-led-training/services-core-implementation
 """
class ClassesSpider(scrapy.Spider):
    name = "classes"

    def start_requests(self):
        f = open("results.csv", "w")
        f.write('"Class Name","Class Location/TimeZone","Start Date","End Date"')
        f.close()
        urls = [
#            'file:///Users/resheti/personal/my_notes/splunk_training_catalog/advanced_searching_and_reporting.html'
#            'https://education.splunk.com/instructor-led-training/advanced-searching-and-reporting-with-splunk-80'
            'https://education.splunk.com/instructor-led-training/splunk-enterprise-80-system-administration',
            'https://education.splunk.com/instructor-led-training/splunk-enterprise-80-data-administration',
            'https://education.splunk.com/instructor-led-training/advanced-searching-and-reporting-with-splunk-80',
            'https://education.splunk.com/instructor-led-training/architecting-splunk-801-enterprise-deployments',
            'https://education.splunk.com/instructor-led-training/troubleshooting-splunk-enterprise-80',
            'https://education.splunk.com/instructor-led-training/splunk-801-cluster-administration',
            'https://education.splunk.com/instructor-led-training/splunk-enterprise-deployment-practical-lab',
            'https://education.splunk.com/instructor-led-training/creating-dashboards-with-splunk-80',
            'https://education.splunk.com/instructor-led-training/services-core-implementation'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        f = open("results.csv", "a")

        
        title = response.css('title::text').get(0)
        self.log('Title %s' % title)
        table = response.css('table.class-schedule')
        rows = table.xpath('//tr')
        # self.log(rows.getall())
        for row in rows:
            columns = row.xpath('td')
            for i in range(len(columns)):
                if (i == 0):
                    class_location = columns[i].css('a::text').get()
                    #self.log("===>Location: [%s]" % class_location)
                else:
                    #self.log(columns[i].getall())
                    for class_date in columns[i].css('a'):
                        class_date_start = class_date.css('span::text').get(0)
                        class_date_end= class_date.css('span::text').get(1)
                        self.log("[%s] [%s] %s -> %s" % (title, class_location, class_date_start, class_date_end))
                        f.write('\n"%s","%s","%s","%s"' % (title, class_location, class_date_start, class_date_end))
        f.close()