<template>
    <div class="container grid-xs form-group" >
      <form action="/users/subscription" method="POST">
        <div class="form-group required">
            <h1><span class="hero bg-gray"></span> You made the right choice !</h1>

            <label for="email" class="form-label">Enter your email address to register</label>
          <input type="email" class="form-input" id="email" name="email"
              placeholder="Votre email" value="" required="required">
          <script>
            $(function () {
              $('#email').focus();
            });
          </script>
        </div>
        <button type="submit" id="submit" name="submit" value="Sign in"
          class="btn btn-primary">Sign up now !</button>
          <a class="btn btn-error" href="/">Back</a>
      </form>
    </div>
</template>



