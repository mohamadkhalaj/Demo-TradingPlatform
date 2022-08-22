try {
    var histSocket = new WebSocket('ws://' + window.location.host + '/ws/histories/');
}
catch (e) {
    var histSocket = new WebSocket('wss://' + window.location.host + '/ws/histories/');
}

var page = 1;
var res = null;
var liveRequest = false;
var newId = -1;
var parent = document.getElementById("histories");

histSocket.onopen = function(e){
    console.log('socket connected');  
    pagination(histSocket);
    histSocket.send(JSON.stringify({"page": page}))
}

histSocket.onmessage = function(e){
    
    data = JSON.parse(e.data);

    var title = document.getElementById("hisrtoryTitle");
    var tableHeader = document.getElementById("tableHeader");
    tableHeader.classList.remove('d-none');
    // tableHeader.classList.add('d-block');
    title.innerText = 'Latest Transactions';
    length = Object.keys(data).length;
    isNew = data["0"]["newHistory"]
    is_complete = length && data["0"]["complete"]

    if(!is_complete || length == 0){
        return
    }
    if(isNew == false){
        liveRequest = false;
        if(res == 'add'){
            page ++;
        }else if(res == 'sub'){
            page --;
        }
        document.getElementById("paginationText").innerText = `${page}`;

        parent.innerHTML = ``;
        for(let i=0; i<length; i++){
            createElems(i);
        }
        fillElems(data);
    }
    else{
        if(page == 1){
            liveRequest = true;
            createElems(newId);
            fillElems(data);
            newId --;
            updateCounters();
        }
    }
    
}

histSocket.onclose = function(e){
    console.log('socket disconnected');
}

function createElems(i){
  
    var tr = document.createElement("tr");
    var number = document.createElement("td");
    var pair = document.createElement("td");
    var type = document.createElement("td");
    var time = document.createElement("td");
    var pairPrice = document.createElement("td");
    var amount = document.createElement("td");
    var price = document.createElement("td");
    
    tr.id = i+"_tr";
    number.id = i+"_number";
    pair.id = i+"_pair";
    type.id = i+"_type";
    time.id = i+"_time";
    pairPrice.id = i+"_pairPrice";
    amount.id = i+"_amount";
    price.id = i+"_price";

    tr.appendChild(number);
    tr.appendChild(pair);
    tr.appendChild(type);
    tr.appendChild(time);
    tr.appendChild(pairPrice);
    tr.appendChild(amount);
    tr.appendChild(price);

    if(liveRequest){
        if(parent.childElementCount == 10){
            parent.removeChild(parent.lastChild);
        }
        parent.prepend(tr);
    }
    else{
        parent.appendChild(tr);
    }
   
}
function fillElems(data){
    rowNumber = (page-1) * 10 + 1;
    Object.keys(data).forEach(function(item, index){
        obj = data[index];

        if(liveRequest){
            ind = newId;
        }else{
            ind = index;
        }
        
        document.getElementById(ind + "_number").innerText = rowNumber;
        document.getElementById(ind + "_pair").innerText = `${obj["pair"]}`;

        typeElem = document.getElementById(ind + "_type");
        typeElem.innerText = `${obj["type"]}`;

        if(obj["type"] == "sell"){
            typeElem.style.color = '#ff231f';
        }else{
            typeElem.style.color = '#26de81';
        }

        document.getElementById(ind + "_time").innerText = `${obj["datetime"]}`;
        document.getElementById(ind + "_pairPrice").innerText = `${obj["pairPrice"]}`;
        document.getElementById(ind + "_amount").innerText = `${parseFloat(obj["amount"].split(' ')[0]).toFixed(4)} ${obj["amount"].split(' ')[1]}`;
        document.getElementById(ind + "_price").innerText = `${(obj['pairPrice'] * obj['amount'].split(' ')[0]).toFixed(2)}`;

        rowNumber += 1;
    })

}
function updateCounters(){
    parent.childNodes.forEach(function(item, index){
        if (item.firstChild){
            item.firstChild.innerText = index + 1;
        }
    })
}
function pagination(){
    document.getElementById('paginationPrev').addEventListener ('click',  function(e){
        if(page > 1){
            res = 'sub';
            histSocket.send(JSON.stringify({"page": page - 1}));
        }
    })
    document.getElementById('paginationNext').addEventListener ('click',  function(e){
        if(parent.childElementCount == 10){
            res = 'add';
            histSocket.send(JSON.stringify({"page": page + 1}));
        }
    })  
}