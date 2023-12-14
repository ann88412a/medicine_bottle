var medicines = {};
var med_order;
 

function create_json(med, checked){
    if(checked){
        medicines[med] = {
            verification:null,
            dilution:-1,
            injection:-1,
            way:null,
            after_dilution:null
        }
    }
    else{
        delete medicines[med];
    }
    createtbl();
}


var medicine_keys
function createtbl() {
    let table = document.createElement('table');
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');
    table.border = "3";
    table.appendChild(thead);
    table.appendChild(tbody);
    var globaldiv = document.getElementById("medtable");
    if (globaldiv) {
        globaldiv.innerHTML = "";
        globaldiv.appendChild(table);
    }
    // Creating and adding data to first row of the table
    let row_1 = document.createElement('tr');
    let heading_1 = document.createElement('th');
    heading_1.innerHTML = "No.";
    let heading_2 = document.createElement('th');
    heading_2.innerHTML = "藥劑名稱";
    let heading_3 = document.createElement('th');
    heading_3.innerHTML = "驗證藥物";
    let heading_4 = document.createElement('th');
    heading_4.innerHTML = "稀釋總量";
    let heading_5 = document.createElement('th');
    heading_5.innerHTML = "施打總量";
    let heading_6 = document.createElement('th');
    heading_6.innerHTML = "給藥途徑";

    row_1.appendChild(heading_1);
    row_1.appendChild(heading_2);
    row_1.appendChild(heading_3);
    row_1.appendChild(heading_4);
    row_1.appendChild(heading_5);
    row_1.appendChild(heading_6);
    thead.appendChild(row_1);

    
    medicine_keys = Object.keys(medicines);
    for (i=0; i<medicine_keys.length; i++) {
        // Creating and adding data to second row of the table
        let row_2 = document.createElement('tr');
        let row_2_data_1 = document.createElement('td');
        row_2_data_1.style.textAlign = "center";
        row_2_data_1.innerHTML = i+1;
        let row_2_data_2 = document.createElement('td');
        row_2_data_2.innerHTML = medicine_keys[i];
        row_2_data_2.style.textAlign = "center";
        let row_2_data_3 = document.createElement('td');
        row_2_data_3.style.textAlign = "center";
        if (medicines[medicine_keys[i]]['verification'] != null){
            row_2_data_3.innerHTML = "已掃描<br>";

            let button = document.createElement('button');
            button.innerHTML = "重新驗證藥物"; // 設置按鈕的文本
            button.name = "syringe_verification";
            button.style.color = "white";
            button.style.fontFamily = "verdana";
            button.style.fontSize = "18px";
            button.style.borderRadius = "10px";
            button.style.backgroundColor = "orange";
            button.style.textAlign = "center";
            
            // 添加點擊事件處理程序
            button.addEventListener('click', (function(index) {
                return function(){
                    JumpToPage(1);
                    Getbutton_id(1, index);
                    Getbutton_id(2, index);
                    Getbutton_id(3, index);
                    Getbutton_id(6, index);
                    ChangeTitle(1);
                    console.log(index);
                };
            })(i));

            // 將按鈕添加到 row_2_data_3 元素中
            row_2_data_3.appendChild(button);
        }
        else{
            row_2_data_3.innerHTML = '<button name="syringe_verification" style="color: white;font-family:verdana;font-size:18px;border-radius: 10px;background-color: green;text-align:center;" onclick="JumpToPage(1);Getbutton_id(1,'+i+');Getbutton_id(2, '+i+');Getbutton_id(6, '+i+');Getbutton_id(3, '+i+');ChangeTitle(1);test('+i+');">驗證</button>';
            row_2_data_3.style.textAlign = "center";
        }
        
        let row_2_data_4 = document.createElement('td');
        row_2_data_4.style.textAlign = "center";
        if (medicines[medicine_keys[i]]['dilution'] < 0){
            row_2_data_4.innerHTML = '尚未輸入';
        }
        else{
            row_2_data_4.innerHTML = medicines[medicine_keys[i]]['dilution'] + "/ml";
        }

        let row_2_data_5 = document.createElement('td');
        row_2_data_5.style.textAlign = "center";
        if (medicines[medicine_keys[i]]['injection']<0){
            row_2_data_5.innerHTML = '尚未辨識';
        }
        else{
            row_2_data_5.innerHTML = medicines[medicine_keys[i]]['injection'] + "/ml  " ;
        }
  
        
        
        let row_2_data_6 = document.createElement('td');
        
        var way_result = ""
        if (medicines[medicine_keys[i]]['way'] != null){
            row_2_data_6.innerHTML = medicines[medicine_keys[i]]['way'];
            row_2_data_6.style.textAlign = "center";
        }
        else{
            row_2_data_6.innerHTML = '尚未選擇';
            row_2_data_6.style.textAlign = "center";
        }

        row_2.appendChild(row_2_data_1);
        row_2.appendChild(row_2_data_2);
        row_2.appendChild(row_2_data_3);
        row_2.appendChild(row_2_data_4);
        row_2.appendChild(row_2_data_5);
        row_2.appendChild(row_2_data_6);
        tbody.appendChild(row_2);
    }
    
}
window.addEventListener("load",createtbl);


function test(i){
    console.log(i);
}


function ChangeTitle(i) {
    var nobarElement = document.getElementById("title");

    switch(i){
        case 0:
            nobarElement.innerHTML = "指示 4<br>開始給針劑";
            break;
        case 1:
            nobarElement.innerHTML = "指示 5<br>確認藥瓶上有無條碼";
            break;
        case 2:
            nobarElement.innerHTML = "指示 6<br>拿掃描機<br>掃藥瓶上的條碼";
            break;
        case 3:
            nobarElement.innerHTML = "指示 6<br>點選你的藥物";
            break;
        case 4:
            nobarElement.innerHTML = "指示 7<br>選擇空針與開始稀釋藥物";
            break;
        case 5:
            nobarElement.innerHTML = "指示 8<br>將抽取好給病人劑量的針具依照圖示放入辨識盒";
            break;
        case 6:
            nobarElement.innerHTML = "指示 9<br>進行注射";
            break;
        case 7:
            nobarElement.innerHTML = "指示 10<br>選取給藥途徑";
            break;
    }

}


function JumpToPage(page) {
    for (let i = 0; i <= 8; i++) {
        document.getElementById(`page${i}`).hidden = (i === page) ? false : true;
    }
}


function tabSW(evt, tab_ID) {
var i, tabcontent, tablinks;

// 使用 class="tabcontent" 獲取所有元素並隱藏它們
tabcontent = document.getElementsByClassName("tabcontent");
for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
}

// 獲取所有帶有 class="tablinks" 的元素並删除類 "active"
tablinks = document.getElementsByClassName("tablinks");
for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
}

// 顯示當前選項卡，並添加"活動"選項卡 類到打開選項卡的按鈕
document.getElementById(tab_ID).style.display = "block";
evt.currentTarget.className += " active";
}

function Getbutton_id(page_type, button_id){
    if(page_type=='2'){  //劑量
        document.getElementsByName("injection_button_id").value= button_id;
    }
    else if(page_type=='3'){  //給藥途徑
        document.getElementsByName("way_button_id").value= button_id;
    }
    else if (page_type=='6'){ //稀釋
        document.getElementsByName("dilution_button_id").value = button_id;
    }
    else if(page_type=='1'){
        document.getElementsByName("verification_button_id").value = button_id;
    }

    }

      


function GetOption(p){

    if(p==8){
        if ($('input[name=injection_info]:checked').val()){
            medicines[medicine_keys[document.getElementsByName("way_button_id").value]]['way'] = [$('input[name=injection_info]:checked').val()]; 
            JumpToPage(0);
            ChangeTitle(0);
        }
        else{
            alert('請選擇針劑給藥途徑!');
        }
    }       
    else if(p==9){
        if ($('input[name=injection_info]:checked').val()==undefined){
            alert('請選擇注射部位!');
        }
        else if ($('input[name=injection_info_site]:checked').val()==undefined){
            alert('請選擇注射角度!');
        }
        else{
            medicines[medicine_keys[document.getElementsByName("way_button_id").value]]['way'] = [$('input[name=injection_info]:checked').val(), $('input[name=injection_info_site]:checked').val()]; 
            JumpToPage(0);
            ChangeTitle(0);
        }
    }
    else if(p==6){
        // 防呆功能
        var selectElement = document.getElementsByName("syringe_type")[0];
        var selectedValue = selectElement.value;

        var inputValue = document.getElementsByName("syringe_diluent_value")[0].value;
        // 使用正則表達式檢查輸入值是否為整數
        var isInteger = /^\d+$/.test(inputValue);

        if (selectedValue === "") {
            alert("尚未選擇空針樣式!");
        }
        else if (!isInteger){
            alert("請輸入稀釋數值!");
        }
        else{
            JumpToPage(2);
        }


        medicines[medicine_keys[document.getElementsByName("dilution_button_id").value]]['dilution'] = $('input[name="syringe_diluent_value"]').val();

        // console.log($('input[name="syringe_diluent_value"]').val());
    }

    console.log(medicines[medicine_keys[0]]);
    console.log(medicines[medicine_keys[1]]);

    createtbl();
    }

function Barcode(on_off){
    dan.push('Barcode-I',[client_uid,'Device_Demo','syringe', on_off]);
}


function Syringe_recognition(){
    dan.push('Syringe-I',[client_uid,'Device_Demo', $("select[name='syringe_type']").val(), 1]);
}