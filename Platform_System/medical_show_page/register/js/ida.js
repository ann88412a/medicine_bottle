 $(function(){
        csmapi.set_endpoint ('https://6.iottalk.tw');
        var profile = {
                'dm_name': 'medical_show_page',          
                'idf_list':[],
                'odf_list':[show],
                'd_name': 'medical_show_page_1',
        };
		
        

        function show(data){
                console.log(data)
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
