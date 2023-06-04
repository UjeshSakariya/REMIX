  <h6 class = 'font'> Add Caption</h6>
    <br>
    <div class="mb-3">
        <input type="text" class="form-control" name = 'caption' id = 'caption' >
        <div  class="form-text">If you wish to caption your post, please enter a message</div>
      </div>
    <button class="btn btn-primary" type="submit">submit</button>

         cursor.execute('SELECT * FROM feed')
     data = cursor.fetchone()
     name = data[1]
     print(name)
     img = data[2]
     title = data[4]

     caption = data[3]
     with open(f'feed/{title}', 'x') as file:
          print('success')
     with open(f'feed/{title}', 'wb') as file:
        file.write(img)
     print("[DATA] : The following file has been written to the project directory: ", 'feed')



function sendData(user,postnum) {
            let user = user
            let postnum = postnum
            $.ajax({
                url: '/process',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 'users': user, 'postnum': postnum}),
                success: function(response) {
                    document.getElementById('output').innerHTML = response.result;
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }

function validateForm() {
            let x = document.forms["comment"].value;
            if (x == "") {
                alert("You must add a comment");
                return false;
            }
        }