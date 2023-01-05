 $(function(){
        csmapi.set_endpoint ('https://6.iottalk.tw');
        var mac_addr = '9d12a9a36e77';
        var profile = {
		    'dm_name': 'medical_show_page',          
            'idf_list':[],
            'odf_list':[show],
            'd_name': 'medical_show_page_1',
        };

		
        function show(data){
            var pills = JSON.parse(data[2]);
            
            $('.ODF_ID')[0].innerText=data[0];
            $('.ODF_pID')[0].innerText=data[1];

            if (pills['Dilatrend 25mg/tab'] >= 1 && pills['Dilantin'] == 0) 
            {
                $('.Dilatrend')[0].innerText='O';
            }else{
                $('.Dilatrend')[0].innerText='X';
            } 

            if (pills['Requip F.C 0.25mg/tab'] >= 1)
            {
                $('.Requip')[0].innerText='X';
            }else{
                $('.Requip')[0].innerText='O';
            }

            if (pills['Repaglinide 1mg/tab'] >= 1)
            {
                $('.Repaglinide')[0].innerText='X';
            }else{
                $('.Repaglinide')[0].innerText='O';
            } 

            if (pills['Transamin 250mg/tab'] >= 1)
            {
                $('.Transamin')[0].innerText='X';
            }else{
                $('.Transamin')[0].innerText='O';
            }

            if (pills['Bokey 100mg/tab'] == 1)
            {
                $('.Bokey')[0].innerText='O';
            }else{
                $('.Bokey')[0].innerText='X';
            }
            
            if (pills['Zocor 20 mg/tab'] == 1)
            {
                $('.Zocor')[0].innerText='O';
            }else{
                $('.Zocor')[0].innerText='X';
            }

            if (pills['FLU-D (Fluconazole) 50mg/tab'] >= 1)
            {
                $('.FLU-D')[0].innerText='X';
            }else{
                $('.FLU-D')[0].innerText='O';
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
