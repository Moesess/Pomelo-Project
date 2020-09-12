$(document).ready(function() {
    $(function ()
    {
         $("#id_first_name").popover({title: 'Twoje imię', trigger: 'focus', content: "Wpisz tu swoje prawdziwe imię"});
         $("#id_last_name").popover({title: 'Twoje nazwisko', trigger: 'focus', content: "Wpisz tu swoje prawdziwe nazwisko"});
         $("#id_email").popover({title: 'Twój adres e-mail', trigger: 'focus', content: "Wpisz tu swój adres e-mail, na który wyślemy Ci potwierdzenie rejestracji"});
         $("#id_username").popover({title: 'Twoja nazwa użytkownika', trigger: 'focus', content: "Wpisz tu swoją nazwę użytkownika, od 4 do 20 znaków, niedozwolone znaki specjalne"});
         $("#id_password1").popover({title: 'Hasło użytkownika', trigger: 'focus', content: "Od 8 do 20 znaków, jedna cyfra oraz jedna wielka litera, może zawierać znaki !@#$%^&*"});
         $("#id_password2").popover({title: 'Powtórz hasło użytkownika', trigger: 'focus', content: "Hasła muszą się zgadzać"});
    });
});

$(function() {
      // Initialize form validation on the registration form.
      // It has the name attribute "registration"
      $("form[name='registration']").validate({
        // Specify validation rules
        rules: {
          // The key name on the left side is the name attribute
          // of an input field. Validation rules are defined
          // on the right side
          first_name: "required",
          last_name: "required",
          email: {
                required: true,
            // Specify that email should be validated
            // by the built-in "email" rule
                email: true,
                pattern: /^([1-zA-Z0-1@.\s]{1,255})$/
          },
          password1: {
                required: true,
                pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[\w@#$%^&*!?]{8,20}$/
          },
            password2: {
                required: true,
                equalTo: "#id_password1"
            },
            username: {
              required: true,
                pattern: /^[a-zA-Z0-9]{4,20}$/
            }
        },
        // Specify validation error messages
        messages: {
          first_name: "Uzupełnij imię",
          last_name: "Uzupełnij nazwisko",
          password1: {
            required: "Uzupełnij hasło",
              pattern: "Hasło niezgodne z wymaganiami"
          },
            password2: {
                required: "Powtórz hasło",
                equalTo: "Hasła nie są identyczne"
            },
            username: {
              required: "Uzupełnij nazwę użytkownika",
                pattern: "Nazwa niezgodna z wymaganiami"
            },
          email: "Wpisz poprawny e-mail"
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
          form.submit();
        }
      });
    });
