 $(function(){
        csmapi.set_endpoint ('https://1.iottalk.tw');
        var profile = {
		    'dm_name': 'Medication_Platform',          
			'idf_list':[Barcode_I, Pill_Detect_I, Search_I, Sheet_I],
			'odf_list':[Patient_O, Pill_Detect_Result_O, Search_Result_O],
		        'd_name': 'Medication_Platform',
        };
		

        function testing(data){

        }
        // 1fcc84831da4
        function Barcode_I(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function Pill_Detect_I(data){
            $('.ODF_value')[0].innerText=data[0];
         }

        function Search_I(data){
            $('.ODF_value')[0].innerText=data[0];
        }

        function Sheet_I(data){
            $('.ODF_value')[0].innerText=data[0];
        }

        function Patient_O(data){
            $('.ODF_value')[0].innerText=data[0];
        }

        function Pill_Detect_Result_O(data){
            $('.ODF_value')[0].innerText=data[0];
        }

        function Search_Result_O(data){
            $('.ODF_value')[0].innerText=data[0];
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
