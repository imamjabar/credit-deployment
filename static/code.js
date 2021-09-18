var person_age_, person_income_, person_home_ownership_, person_emp_length_, loan_intent_, loan_grade_, loan_amnt_, loan_int_rate_, loan_percent_income_, cb_person_default_on_file_, cb_person_cred_hist_length_;

$(document).ready(function(){
  // fetch all DOM elements for the input
  person_age_ = document.getElementById("person_age");
  person_income_ = document.getElementById("person_income");
  person_home_ownership_ = document.getElementById("person_home_ownership");
  person_emp_length_ = document.getElementById("person_emp_length");
  loan_intent_ = document.getElementById("loan_intent");
  loan_grade_ = document.getElementById("loan_grade");
  loan_amnt_ = document.getElementById("loan_amnt");
  loan_int_rate_ = document.getElementById("loan_int_rate");
  loan_percent_income_ = document.getElementById("loan_percent_income");
  cb_person_default_on_file_ = document.getElementById("cb_person_default_on_file");
  cb_person_cred_hist_length_ = document.getElementById("cb_person_cred_hist_length");
})

$(document).on('click','.button',function(e){
    // on clicking submit fetch values from DOM elements and use them to make request to our flask API
    var person_age = person_age_.value;
    var person_income = person_income_.value;
    var person_home_ownership = person_home_ownership_.value;
    var person_emp_length = person_emp_length_.value;
    var loan_intent = loan_intent_.value;
    var loan_grade = loan_grade_.value;
    var loan_amnt = loan_amnt_.value;
    var loan_int_rate = loan_int_rate_.value;
    var loan_percent_income = loan_percent_income_.value;
    var cb_person_default_on_file = cb_person_default_on_file_.value;
    var cb_person_cred_hist_length = cb_person_cred_hist_length_.value;
    if(person_age == "" || person_income == "" ||person_home_ownership == ""||person_emp_length == ""||loan_intent == ""||loan_grade == ""||
    	loan_amnt == ""||loan_int_rate == ""||loan_percent_income == ""||cb_person_default_on_file == ""||cb_person_cred_hist_length == ""){
      // you may allow it as per your model needs
      // you may mark some fields with * (star) and make sure they aren't empty here
      alert("empty fields not allowed");
    }
    else{
      // replace <username> with your pythonanywhere username
      // also make sure to make changes in the url as per your flask API argument names
      // var requestURL = "http://127.0.0.1:5000/predict?Age="+Age+"&Sex="+Sex+"&Job="+Job+"&Housing="+Housing+"&saving_account="+saving_account+"&checking_account="+checking_account+"&credit_amount="+credit_amount+"&duration="+duration+"&purpose="+purpose;
      // console.log(requestURL); // log the requestURL for troubleshooting
      
      // $.getJSON(requestURL, function(data) {
      //   console.log(data); // log the data for troubleshooting
      //   prediction = data['result'];
      //   $(".result").html("Prediction is: "+prediction);
      //   $(".result").css({
      //     "color": "#666666",
      //     "text-align": "center"
      //   });
      // });
      
      var data = {
          "person_age": person_age,
          "person_income": person_income, 
          "person_home_ownership": person_home_ownership, 
          "person_emp_length": person_emp_length, 
          "loan_intent": loan_intent, 
          "loan_grade": loan_grade, 
          "loan_amnt": loan_amnt,
          "loan_int_rate": loan_int_rate, 
          "loan_percent_income": loan_percent_income, 
          "cb_person_default_on_file": cb_person_default_on_file,
          "cb_person_cred_hist_length": cb_person_cred_hist_length
      };
      //console.log(data)

      // # https://api.jquery.com/jquery.post/
      // # https://stackoverflow.com/questions/56032972/sending-a-dictionary-from-js-to-flask-via-ajax
      $.ajax({
        url: 'https://credit-scoring-imam.herokuapp.com/predict',
        //url: 'http://127.0.0.1:5000/predict',
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify({data}),
        dataType: "json",
        type: 'POST',
        success: function(response){
            //console.log(response);
            prediction = response['result'];
            $(".result").html("Prediction is: "+prediction);
            $(".result").css({
              "color": "#666666",
              "text-align": "center"
            });
        },
        error: function(error){
            console.log(error);
        }
    });
      // following lines consist of action that would be taken after the request has been read
      // for now i am just changing a <h2> tag's inner html using jquery
      // you may simple do: 
      // alert(prediction);
      e.preventDefault();
    }
  });
