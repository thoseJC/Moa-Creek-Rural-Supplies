document.addEventListener("DOMContentLoaded", function () {
    fetch('/manager/report_panel')
        .then(response => response.json())
        .then(data => {
            createInventoryChart(data.inventory);
            createOrdersPieChart(data.orders);
            createPaymentLineChart(data.payment);
            createShipmentsPieChart(data.shipments);
        });

    function createInventoryChart(data) {
        var chartDom = document.getElementById('inventory-chart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            title: {
                text: 'Inventory Data',
                left: 'center'
            },
            tooltip: {},
            xAxis: {
                type: 'value',
                name: 'Quantity'

            },
            yAxis: {
                type: 'category',
                name: 'Product ID',
                data: data.x_invt_qty
            },
            series: [
                {
                    data: data.y_invt_id,
                    type: 'bar',
                    itemStyle: {
                        color: 'rgb(72,134,152)'
                    }
                }
            ]
        };

        option && myChart.setOption(option);
    }

    function createOrdersPieChart(data) {
        var chartDom = document.getElementById('orders-chart');
        var myChart = echarts.init(chartDom);
        var option;

        var colors = ['rgba(57,105,182,0.89)', '#957DAD', '#D291BC', 'rgba(222,254,200,0.34)', '#FFDFD3'];

        option = {
            title: {
                text: 'Orders Data',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                top: '5%',
                left: 'center'
            },
            series: [
                {
                    name: 'Order Status',
                    type: 'pie',
                    radius: '50%',
                    data: data.x_odrs_status.map((status, index) => ({
                        name: status,
                        value: data.y_odrs_qty[index],
                        itemStyle: {
                            color: colors[index]
                        }
                    })),
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        option && myChart.setOption(option);
    }

    function createPaymentLineChart(data) {
        var chartDom = document.getElementById('payment-chart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            title: {
                text: 'Payment Data',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                name: 'Month',
                data: data.x_pyt_date
            },
            yAxis: {
                type: 'value',
                name: 'Total Payment ($)'
            },
            series: [
                {
                    data: data.y_pyt_total,
                    type: 'line',
                    itemStyle: {
                        color: '#0d87a6'
                    }
                }
            ]
        };

        option && myChart.setOption(option);
    }

    function createShipmentsPieChart(data) {
        var chartDom = document.getElementById('shipments-chart');
        var myChart = echarts.init(chartDom);
        var option;

        var colors = ['#FF9AA2', 'rgba(102,154,69,0.84)', 'rgba(78,146,203,0.7)', 'rgba(121,116,210,0.63)', '#B5EAD7'];
        option = {
            title: {
                text: 'Shipments Data',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                top: '5%',
                left: 'center'
            },
            series: [
                {
                    name: 'Shipment Status',
                    type: 'pie',
                    radius: '50%',
                    data: data.x_spm_status.map((status, index) => ({
                        name: status,
                        value: data.y_spm_qty[index],
                        itemStyle: {
                            color: colors[index]
                        }
                    })),
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        option && myChart.setOption(option);
    }
});
