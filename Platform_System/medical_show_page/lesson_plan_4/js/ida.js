 $(function(){
        csmapi.set_endpoint ('https://1.iottalk.tw');
        var mac_addr = 'c3ad38d013c8';
        var profile = {
		    'dm_name': 'medical_feedback',          
            'idf_list':[save],
            'odf_list':[show],
            'd_name': 'medical_show_page_1',
        };

		function save(){
            console.log('save');
        }
        
        function show(data){
            var datas = JSON.parse(data[0]);
            
            var id_name = datas['id'] + ' ' + datas['name'];
            $('.ODF_ID')[0].innerText= id_name;

            // 1
            var img1 = document.getElementById('paitent img');
            if (datas['barcode_r'] == 'no') 
            {
                img1.src="pic/ok.jpg";
            }else{
                img1.src="pic/wrong.jpeg";
            } 

            paitent_r = '掃描結果：' + datas['barcode'] + ',   您判斷是否正確：' + datas['barcode_r'];
            document.getElementById('paitent r').innerHTML = paitent_r;

            // 2
            var img2 = document.getElementById('2 img');
            if (datas['Dilatrend25'] == 1 && datas['Dilantin'] == 0) 
            {
                img2.src="pic/ok.jpg";
            }else{
                img2.src="pic/wrong.jpeg";
            } 

            r2 = '您給 Dilatrend 25mg/tab 的理由：' + datas['Dilatrend25_r'];
            document.getElementById('2 r').innerHTML = r2;
            r2r = '您給 Dilantin 的理由：' + datas['Dilantin_r'];
            document.getElementById('2 r 2').innerHTML = r2r;

            // 3
            var img3 = document.getElementById('3 img');
            if (datas['Requip'] == 0 && datas['Requip1'] == 0) 
            {
                img3.src="pic/ok.jpg";
            }else{
                img3.src="pic/wrong.jpeg";
            } 

            r3 = '您給 Requip F.C 0.25mg/tab 的理由：' + datas['Requip_r'];
            document.getElementById('3 r').innerHTML = r3;
            r3r = '您給 Requip F.C 1mg 的理由：' + datas['Requip1_r'];
            document.getElementById('3 r 3').innerHTML = r3r;

            // 4
            var img4 = document.getElementById('4 img');
            img4.src="pic/undone.png";
            
            // 5
            var img5 = document.getElementById('5 img');
            if (datas['Repaglinide'] == 0) 
            {
                img5.src="pic/ok.jpg";
            }else{
                img5.src="pic/wrong.jpeg";
            } 

            r5 = '您給 Repaglinide 1mg/tab 的理由：' + datas['Repaglinide_r'];
            document.getElementById('5 r').innerHTML = r5;

            // 6
            var img6 = document.getElementById('6 img');
            if (datas['Transamin'] == 0) 
            {
                img6.src="pic/ok.jpg";
            }else{
                img6.src="pic/wrong.jpeg";
            } 

            r6 = '您給 Transamin 250mg/tab 的理由：' + datas['Transamin_r'];
            document.getElementById('6 r').innerHTML = r6;
           
            // 7 
            
         
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
