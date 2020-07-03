// SIDEBAR TOGGLE
$('#toggle').click(function(){
    $('.ui.sidebar').sidebar('toggle');
});

// SIDEBAR DROPDOWN TAGS
$('#tweet-select').dropdown();

$('#mention-select').dropdown();

// PROFILE MENU DROPDOWN ITEMS
function me(){
    document.getElementById("mlist").style.display = "block";
}

// SIDEBAR RANGE SLIDER
$(document).ready(function(){
    $('#slider1').slider({
        min:20,
        max:100,
        step:10,
        value:10
    });
});


 // DATATABLES PLUGIN SCRIPT
$('.dftable tr:contains("Negativo")').addClass('negative');
$('.dftable td:contains("Negativo")').html("<i class='icon frown outline'></i> Negativo");
$('.dftable tr:contains("Positivo")').addClass('positive');
$('.dftable td:contains("Positivo")').html("<i class='icon smile outline'></i> Positivo");
$('.dftable th:contains("Fecha")').html("<div class='ui teal ribbon label' >Fecha</div>")  
 $(document).ready(function() {
    $('.dftable').DataTable({
        scrollY:500,
        scrollCollapse: true
    });
    $('.dftable tr:contains("Negativo")').addClass('negative');
    $('.dftable td:contains("Negativo")').html("<i class='icon frown outline'></i> Negativo");
    $('.dftable tr:contains("Positivo")').addClass('positive');
    $('.dftable td:contains("Positivo")').html("<i class='icon smile outline'></i> Positivo");
    /*$('#dftable td:contains("https://twitter.com/")').addClass("ui small button");*/
    });
    $('.dftable').bind('page', function(){
        $('.dftable tr:contains("Negativo")').addClass('negative');
        $('.dftable td:contains("Negativo")').html("<i class='icon frown outline'></i> Negativo");
        $('.dftable tr:contains("Positivo")').addClass('positive');
        $('.dftable td:contains("Positivo")').html("<i class='icon smile outline'></i> Positivo");
    });
