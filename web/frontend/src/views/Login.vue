<template>
<div class="login">
    <div class="item">
        <img alt="att-logo" src="../assets/att.png" height="220" width="500"><br>

        <div class="user">
            <div class="col-md-6 col-md-offset-5">
                <div class="input-group">
                    <span class="input-group-text" id="basic-addon1"><font-awesome-icon :icon="['fas', 'user']" size=lg /></span>
                    <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
                </div>
            </div>
        </div>
        <div class="password">
            <div class="col-md-6 col-md-offset-5">
                <div class="input-group">
                    <span class="input-group-text" id="basic-addon1"><font-awesome-icon :icon="['fas', 'lock']" size=lg /></span>
                    <input type="password" class="form-control" placeholder="Password" aria-label="Password" aria-describedby="basic-addon1">
                </div>
            </div>
        </div>


        <br />
        <font-awesome-icon :icon="['fas', 'sing-in-alt']" size=sm />
        <button type="button" class='btn btn-primary btn-lg' @click='toDocker'><font-awesome-icon :icon="['fas', 'sign-in-alt']" size=sm /> Login</button>
        <br>
        <button type="button" class="btn btn-link btn-sm">Forget password</button> |
        <button type="button" class="btn btn-link btn-sm">Create account</button>
    </div>


</div>
</template>

<script>
export default {
    name: 'login',
    data() {
        return {
            content: ''
        }
    },
    methods: {
        toDocker: function(){
            this.$router.push({
                path: "/docker"
            })
        }

    },

}
</script>

<style scoped>
.login {
    background: white;
}

.item {
    padding-top: 100px;
}

.user {
    margin-left: 650px;
    margin-top: 50px;
}
.password {
    margin-left: 650px;
    margin-top: 2px;
}


</style>
