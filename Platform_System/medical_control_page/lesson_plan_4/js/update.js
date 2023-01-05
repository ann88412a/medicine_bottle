async function getvalue()
    {
        const idf_id = document.getElementById('IDF_ID');
        const idf_name = document.getElementById('IDF_name');
        const radios = document.getElementsByName('barcode');
        if (idf_id.value != "")
        {
            var img = document.getElementById('id');
            img.src="pic/ok1.jpeg";
        }else
        {
            var img = document.getElementById('id');
            img.src="";
        }
        if (idf_name.value != "")
        {
            var img = document.getElementById('name');
            img.src="pic/ok1.jpeg";
        }else
        {
            var img = document.getElementById('name');
            img.src="";
        }
        if (radios[0].checked || radios[1].checked)
        {

            var img = document.getElementById('bar');
            img.src="pic/ok1.jpeg";
        }else
        {
            var img = document.getElementById('bar');
            img.src="";
        }
    }

setInterval(getvalue, 1000);

function check_page(n){
    if (n === 1){
        const idf_id = document.getElementById('IDF_ID');
        const idf_name = document.getElementById('IDF_name');
        if (idf_id.value != "" && idf_name.value != ""){
            plusSlides(1);
        }
        else if(idf_id.value == "" && idf_name.value == ""){
            var img1 = document.getElementById('id');
            img1.src="pic/wrong.jpeg";
            var img2 = document.getElementById('name');
            img2.src="pic/wrong.jpeg";
        }
        else if(idf_id.value != ""){
            var img = document.getElementById('name');
            img.src="pic/wrong.jpeg";
        }
        else if(idf_name.value != ""){
            var img = document.getElementById('id');
            img.src="pic/wrong.jpeg";
        }
    }
    else if(n === 3){
        const radios = document.getElementsByName('barcode');
        if (radios[0].checked || radios[1].checked)
        {
            plusSlides(1);
        }else
        {
            var img = document.getElementById('bar');
            img.src="pic/wrong.jpeg";
        }
    }
    else if(n === 4){
        const all_info = JSON.stringify({ id: document.getElementById('IDF_ID').value,
                                            name: document.getElementById('IDF_name').value,
                                            barcode: $('.ODF_value')[0].innerText,
                                            Dilatrend25: document.getElementById('Dilatrend 25mg/tab').value,
                                            Dilatrend25_r: document.getElementById('Dilatrend 25mg/tab r').value,
                                            Requip: document.getElementById('Requip F.C 0.25mg/tab').value,
                                            Requip_r: document.getElementById('Requip F.C 0.25mg/tab r').value,
                                            Repaglinide: document.getElementById('Repaglinide 1mg/tab').value,
                                            Repaglinide_r: document.getElementById('Repaglinide 1mg/tab r').value,
                                            Transamin: document.getElementById('Transamin 250mg/tab').value,
                                            Transamin_r: document.getElementById('Transamin 250mg/tab r').value,
                                            Bokey: document.getElementById('Bokey 100mg/tab').value,
                                            Bokey_r: document.getElementById('Bokey 100mg/tab r').value,
                                            Zocor: document.getElementById('Zocor 20 mg/tab').value,
                                            Zocor_r: document.getElementById('Zocor 20 mg/tab r').value,
                                            FLU: document.getElementById('FLU-D (Fluconazole) 50mg/tab').value,
                                            FLU_r: document.getElementById('FLU-D (Fluconazole) 50mg/tab r').value,
                                            Dilantin: document.getElementById('Dilantin').value,
                                            Dilantin_r: document.getElementById('Dilantin r').value,
                                            Requip: document.getElementById('Requip F.C 1 mg').value,
                                            Requip_r: document.getElementById('Requip F.C 1 mg r').value,
                                            
                                             });
        dan.push('confim', all_info);
    }
    else{
        plusSlides(1);
    }
}

function check_bt(f){
    if (f === 'barcode'){
        dan.push('patient_barcode',[true]);
        // sleep(3000);
        output_patient_barcode_bt = output_patient_barcode_bt + 1;
    }
    else if(f === 'pill'){
        dan.push('pill_detect',[true]);
        output_pill_bt = output_pill_bt + 1;
    }
}