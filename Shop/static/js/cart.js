 $('.plus-cart').click(function(){
//    console.log("Plus Clicked")
    var id= $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
//    console.log(id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
              prod_id:id
        },
        success:function(data){
           eml.innerText = data.quantity
           document.getElementById("amount").innerText=data.amount
           document.getElementById("totalamount").innerText=data.totalamount


        }

    })
})



$('.minus-cart').click(function(){
//    console.log("Plus Clicked")
    var id= $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
//    console.log(id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
              prod_id:id
        },
        success:function(data){
           eml.innerText = data.quantity
           document.getElementById("amount").innerText=data.amount
           document.getElementById("totalamount").innerText=data.totalamount


        }

    })
})


$('.remove-cart').click(function(){
//    console.log("Plus Clicked")
    var id= $(this).attr("pid").toString();
    var eml = this
//    console.log(id)
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
              prod_id:id
        },
        success:function(data){
           console.log("Delete")

           document.getElementById("amount").innerText=data.amount
           document.getElementById("totalamount").innerText=data.totalamount
           eml.parentNode.parentNode.parentNode.parentNode.remove()

        }

    })
})