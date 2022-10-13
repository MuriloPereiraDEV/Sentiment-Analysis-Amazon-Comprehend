function sentiment(){
            
    const txtUser = document.getElementById("txt-user").value;

    const dictValues = {
        txtUser
    }

    const dictValuesJason = JSON.stringify(dictValues)
    console.log(dictValuesJason)

    $.ajax({
        url:"/test",
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify(dictValuesJason),
        success: function(data){
            function addInformation(info){

                var elementLang = document.querySelector(".language")
                var elementSent = document.querySelector(".sentiment")

                elementLang.innerHTML = ''
                elementSent.innerHTML = ''
                
                elementLang.innerHTML = '<h1 class="language-h1" id="language-h1">'+info[0]+'</h1>'
                elementSent.innerHTML = '<h1 class="sentiment-h1" id="sentiment-h1">'+info[1]+'</h1>'

            }
            addInformation(data)
        }
    })
}