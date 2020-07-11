var m;
var y;
var dy;
var d = new Date();
var month_name = ['January','February','March','April','May','June','July','August','September','October','November','December'];
var month = d.getMonth();   //0-11
var year = d.getFullYear(); //2019
var today_date = d.getDate();
var first_date = month_name[month] + " " + 1 + " " + year;
//September 1 2014
var tmp = new Date(first_date).toDateString();
//Mon Sep 01 2014 ...
var first_day = tmp.substring(0, 3);    //Mon
var day_name = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
var full_day_name = ['sunday','monday','tuesday','wednesday','thursday','frieday','saturday'];
var day_no = day_name.indexOf(first_day);   //1
var days = new Date(year, month+1, 0).getDate();    //30
//Tue Sep 30 2014 ...
var old;

window.onload = function() 
{
    var monday = document.getElementById('monday').value
    var tuesday = document.getElementById('tuesday').value
    var wednesday = document.getElementById('wednesday').value
    var thursday = document.getElementById('thursday').value
    var frieday = document.getElementById('frieday').value
    var saturday = document.getElementById('saturday').value
    y = year;
    m = month_name[month];
    dy = day_no;
    var j = 0;
    for(var i=0;i<11;i++)
    {
        var mon = month + i;
        if(mon<12)
        {
            var sel = null;
            sel = document.getElementById("calendar-month-year")
            var opt = document.createElement('option')
            opt.appendChild(document.createTextNode(month_name[mon]+" "+year))
            opt.value = month_name[mon]+" 1 "+year;
            if(sel != null)
                sel.appendChild(opt);
        }
        else if(j<month)
        {
            var sel = null;
            sel = document.getElementById("calendar-month-year")
            var opt = document.createElement('option')
            opt.appendChild(document.createTextNode(month_name[j]+" "+(year+1)))
            opt.value = month_name[j]+" 1 "+(year+1);
            if(sel != null)
                sel.appendChild(opt);
            j += 1;
        }
    }
    var calendar = get_calendar(day_no, days);
    old = document.getElementById("calendar-dates").appendChild(calendar);
    changed_month();
}
function changed_month()
{
    var sel = document.getElementById("calendar-month-year").value
    var mon = new Date(sel).getMonth()
    m = month_name[mon];
    tmp = new Date(sel).toDateString()
    y = tmp.substring(11,15)
    first_day = tmp.substring(0, 3);
    day_no = day_name.indexOf(first_day);
    dy = day_no;
    days = new Date(y, mon+1, 0).getDate();
    calendar = get_calendar(day_no, days);
    document.getElementById("calendar-dates").removeChild(old)
    old = document.getElementById("calendar-dates").appendChild(calendar)
}

function get_calendar(day_no, days){
    var table = document.createElement('table');
    var tr = document.createElement('tr');
    
    //row for the day letters
    for(var c=0; c<=6; c++){
        var td = document.createElement('td');
        td.innerHTML = "SMTWTFS"[c];
        tr.appendChild(td);
    }
    table.appendChild(tr);
    
    //create 2nd row
    tr = document.createElement('tr');
    var c;
    for(c=0; c<=6; c++){
        if(c == day_no){
            break;
        }
        var td = document.createElement('td');
        td.innerHTML = "";
        tr.appendChild(td);
    }
    
    var count = 1;
    for(; c<=6; c++){
        var td = document.createElement('td');
        if(c==0)
            td.innerHTML = count;
        else
            if(m == month_name[month])
            {
                if(count < today_date)
                    td.innerHTML = count;
                else
                {
                    if(c==1 && monday.value=='1')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==2 && tuesday.value=='2')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==3 && wednesday.value=='3')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==4 && thursday.value=='4')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==5 && frieday.value=='5')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==6 && saturday.value=='6')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else
                        td.innerHTML = count;
                }
            }
            else
            {
                    if(c==1 && monday.value=='1')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==2 && tuesday.value=='2')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==3 && wednesday.value=='3')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==4 && thursday.value=='4')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==5 && frieday.value=='5')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==6 && saturday.value=='6')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else
                        td.innerHTML = count;
            }
        count++;
        tr.appendChild(td);
    }
    table.appendChild(tr);
    
    //rest of the date rows
    for(var r=3; r<=7; r++){
        tr = document.createElement('tr');
        for(var c=0; c<=6; c++){
            if(count > days){
                table.appendChild(tr);
                return table;
            }
            var td = document.createElement('td');
            if(c==0)
                td.innerHTML = count;
            else
                if(m == month_name[month])
            {
                if(count < today_date)
                    td.innerHTML = count;
                else
                {
                    if(c==1 && monday.value=='1')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==2 && tuesday.value=='2')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==3 && wednesday.value=='3')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==4 && thursday.value=='4')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==5 && frieday.value=='5')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==6 && saturday.value=='6')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else
                        td.innerHTML = count;
                }
            }
            else
            {
                    if(c==1 && monday.value=='1')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==2 && tuesday.value=='2')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==3 && wednesday.value=='3')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==4 && thursday.value=='4')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==5 && frieday.value=='5')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else if(c==6 && saturday.value=='6')
                        td.innerHTML = "<a href=/appointment/schedule/"+count+"/"+m+"/"+y+"/"+c+" class='link'>"+count+"</a>";
                    else
                        td.innerHTML = count;
            }
            count++;
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
	return table;
}