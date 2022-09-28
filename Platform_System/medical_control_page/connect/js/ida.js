 $(function(){
        csmapi.set_endpoint ('https://6.iottalk.tw');
        var mac_addr = 'a3b571f17654';
        var profile = {
		    'dm_name': 'medical_control',          
			'idf_list':[barcode, confirm, pill_yolo],
			'odf_list':[barcode_result, pill_yolo_done],
		        'd_name': 'medical_control_page_1',
        };

		
        function Dummy_Sensor(){
            return Math.random();
        }

        function Dummy_Control(data){
           $('.ODF_value')[0].innerText=data[0];
        }
        function barcode(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function confirm(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function pill_yolo(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function barcode_result(data){
            console.log(data)
            return Math.random();
        }

        function pill_yolo_done(data){
            console.log(data)
            return Math.random();
        }
      
/*******************************************************************/                
        function ida_init(){
	    console.log(profile.d_name);
	}
        var ida = {
            'ida_init': ida_init,
        }; 
        dai(profile,ida);     
});
