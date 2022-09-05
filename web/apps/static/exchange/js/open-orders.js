try {
    var openOrdersSocket = new WebSocket('ws://' + window.location.host + '/ws/open-orders/');
}
catch (e) {
    var openOrdersSocket = new WebSocket('wss://' + window.location.host + '/ws/open-orders/');
}

var page = 1;
var res = null;
var liveRequest = false;
var newId = -1;
var parent = document.getElementById("histories");

openOrdersSocket.onopen = function(e){
    console.log('socket connected');  
    pagination(openOrdersSocket);
    openOrdersSocket.send(JSON.stringify({"page": page}))
}

openOrdersSocket.onmessage = function(e){
    
    data = JSON.parse(e.data);

    var title = document.getElementById("hisrtoryTitle");
    var tableHeader = document.getElementById("tableHeader");
    tableHeader.classList.remove('d-none');
    // tableHeader.classList.add('d-block');
    title.innerText = 'Open orders';
    length = Object.keys(data).length;
    let live = length && data[0]['header'];

    if(length == 0){
        return
    }
    if(live){
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

openOrdersSocket.onclose = function(e){
    console.log('socket disconnected');
}

function createElems(i){
  
    var tr = document.createElement("tr");
    var number = document.createElement("td");
    var pair = document.createElement("td");
    var type = document.createElement("td");
    var pairPrice = document.createElement("td");
    var amount = document.createElement("td");
    var price = document.createElement("td");

    var cancelBtn = document.createElement("button");
    cancelBtn.innerText = "cancel";
    cancelBtn.classList.add(...['btn', 'btn-primary-outline', 'green']);
    cancelBtn.setAttribute('data-id', i)
    cancelBtn.onclick = function(e){
        openOrdersSocket.send(JSON.stringify({"cancel":[parseInt(this.dataset.id)]}));
        tr.remove()
        res = null;
        openOrdersSocket.send(JSON.stringify({"page": page}));
    }

    tr.id = i+"_tr";
    number.id = i+"_number";
    pair.id = i+"_pair";
    type.id = i+"_type";
    pairPrice.id = i+"_pairPrice";
    amount.id = i+"_amount";
    price.id = i+"_price";
    cancelBtn.id = i+"_cancel";

    tr.appendChild(number);
    tr.appendChild(pair);
    tr.appendChild(type);
    tr.appendChild(pairPrice);
    tr.appendChild(amount);
    tr.appendChild(price);
    tr.appendChild(cancelBtn);

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

    Object.keys(data).forEach(function(item, index){
        obj = data[index];

        if(liveRequest){
            ind = newId;
        }else{
            ind = index;
        }

        document.getElementById(ind + "_number").innerText = index + 1;
        document.getElementById(ind + "_pair").innerText = `${obj["pair"]}`;

        typeElem = document.getElementById(ind + "_type");
        typeElem.innerText = `${obj["type"]}`;

        if(obj["type"] == "sell"){
            typeElem.style.color = '#ff231f';
        }else{
            typeElem.style.color = '#26de81';
        }

        document.getElementById(ind + "_cancel").setAttribute('data-id', obj["id"]);
        document.getElementById(ind + "_pairPrice").innerText = `${obj["pairPrice"]}`;
        document.getElementById(ind + "_amount").innerText = `${parseFloat(obj["amount"].split(' ')[0]).toFixed(4)} ${obj["amount"].split(' ')[1]}`;
        document.getElementById(ind + "_price").innerText = `${(obj['pairPrice'] * obj['amount'].split(' ')[0]).toFixed(2)}`;

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
            openOrdersSocket.send(JSON.stringify({"page": page - 1}));
        }
    })
    document.getElementById('paginationNext').addEventListener ('click',  function(e){
        if(parent.childElementCount == 10){
            res = 'add';
            openOrdersSocket.send(JSON.stringify({"page": page + 1}));
        }
    })  
}