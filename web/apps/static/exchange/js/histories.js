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
    histSocket.send(JSON.stringify({'page': page}))
}

histSocket.onmessage = function(e){
    
    data = JSON.parse(e.data);
    length = Object.keys(data).length;

    var title = document.getElementById("hisrtoryTitle");
    var tableHeader = document.getElementById("tableHeader");
    tableHeader.classList.remove('d-none');
    // tableHeader.classList.add('d-block');
    title.innerText = 'Latest Transactions';
    
    if(length > 0){

        header = data["0"]["header"];
        if(header == 'hist_responses'){

            liveRequest = false;
            if(res == 'add'){
                page ++;
            }else if(res == 'sub'){
                page --;
            }
            console.log('page', page);
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

        document.getElementById(ind + "_time").innerText = `${obj["date"]}`;
        document.getElementById(ind + "_pairPrice").innerText = `${obj["pairPrice"]}`;
        document.getElementById(ind + "_amount").innerText = `${parseFloat(obj["amount"]).toFixed(5)}`;
        document.getElementById(ind + "_price").innerText = `${obj["price"].toFixed(2)}`;

    })

}
function updateCounters(){
    parent.childNodes.forEach(function(item, index){
        item.firstChild.innerText = index + 1;    
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
