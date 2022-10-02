 $(function(){
        csmapi.set_endpoint ('https://6.iottalk.tw');
        var mac_addr = 'a3b571f17654';
        var profile = {
		    'dm_name': 'medical_control',          
			'idf_list':[barcode, confirm, pill_yolo],
			'odf_list':[barcode_result, pill_yolo_done],
		        'd_name': 'medical_control_page_1',
        };

		
        function barcode(){
            
         }

        function confirm(){
            
         }

        function pill_yolo(){
            
         }

        function barcode_result(data){
            // console.log
            $('.ODF_value')[0].innerText=data[0];
        }

        function pill_yolo_done(data){
            if (data[0] == true)
            {
                $('.ODF_yolo')[0].innerText = '藥丸確認完成';
            }else{
                $('.ODF_yolo')[0].innerText = 'waiting...';
            }
            
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
