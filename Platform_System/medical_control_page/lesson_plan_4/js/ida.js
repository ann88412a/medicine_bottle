 $(function(){
        csmapi.set_endpoint ('https://1.iottalk.tw');
        var profile = {
		    'dm_name': 'medical_control',          
			'idf_list':[confirm, patient_barcode, pill_detect],
			'odf_list':[output_patient_barcode, output_pill],
		        'd_name': 'medical_control_page_1',
        };

		
        function confirm(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function patient_barcode(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function pill_detect(data){
            $('.ODF_value')[0].innerText=data[0];
        }

        
        function output_patient_barcode(data){
            console.log(data)
            return Math.random();
        }

        function output_pill(data){
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
