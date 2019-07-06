import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NguiMapModule} from '@ngui/map';
import * as Chartist from 'chartist';


declare var $:any;
declare var google: any;
declare interface TableData {
    headerRow: string[];
    dataRows: string[][];
}

@Component({
    selector: 'dashboard-cmp',
    moduleId: module.id,
    templateUrl: 'dashboard.component.html'
})

export class DashboardComponent implements OnInit{
  public tableData1: TableData;
  public tableData2: TableData;
  employeeData: JSON;
  employee:JSON;

    constructor(private httpClient: HttpClient) {
    }

    ngOnInit(){
      this.tableData1 = {
          headerRow: [ 'Incident No.', 'Caller Name', 'Location', 'Lat Long', 'Remarks'],
          dataRows: [
              ['201907061', 'Pang Sheng Wei', 'Suntec City', '234556', 'I Suck Cock'],
              ['201907062', 'Minerva Hooper', 'Curaçao', 'Sinaai-Waas', '$23,789'],
              ['201907063', 'Sage Rodriguez', 'Netherlands', 'Baileux', '$56,142'],
              ['201907064', 'Philip Chaney', 'Korea, South', 'Overland Park', '$38,735'],
              ['201907065', 'Doris Greene', 'Malawi', 'Feldkirchen in Kärnten', '$63,542'],
              ['201907066', 'Mason Porter', 'Chile', 'Gloucester', '$78,615']
          ]
      };

        var dataSales = {
          labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
          series: [
             [287, 385, 490, 562, 594, 626, 698, 895, 952],
            [67, 152, 193, 240, 387, 435, 535, 642, 744],
            [23, 113, 67, 108, 190, 239, 307, 410, 410]
          ]
        };

        var optionsSales = {
          low: 0,
          high: 1000,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: true,
          showPoint: false,
        };

        var responsiveSales: any[] = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        new Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);


        var data = {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 543, 520, 680, 653, 753, 326, 434, 568, 610, 756, 895],
            [230, 293, 380, 480, 503, 553, 600, 664, 698, 710, 736, 795]
          ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions: any[] = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        new Chartist.Line('#chartActivity', data, options, responsiveOptions);

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        new Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        new Chartist.Pie('#chartPreferences', {
          labels: ['62%','32%','6%'],
          series: [62, 32, 6]
        });
        
        this.httpClient.get('http://127.0.0.1:5000/employees').subscribe(data => {
          this.employeeData = data as JSON;
          console.log(this.employeeData);
          console.log("COCKSUCKER");
        })
    }
}