<template>
    <v-layout column justify-center align-center>
      <v-btn color="success" to="/app/create">
        CREATE
      </v-btn>
      <v-data-table
        :headers="headers"
        :items="listData"
        class="elevation-0"
        >
        <template slot="items" slot-scope="props">
          <tr>
            <td>{{ props.item.id }}</td>
            <td>{{ props.item.article_title }}</td>
            <td>{{ props.item.article_description }}</td>
            <td>
              <v-btn color="error" @click="deleteArticle(props.item.id)">
                DELETE
              </v-btn>
              <v-btn color="primary" :to="`/app/edit/${props.item.id}`">
                EDIT
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-layout>
</template>

<script>
    export default {
        name: "index",
        data() {
          return {
            listData: [],
            headers: [
              {
                text: 'Id',
                value: 'id'
              },
              {
                text: 'Article Heading',
                value: 'article_title'
              },
              {text: 'Article Description', value: 'article_description'},
              {text: 'Action', value: 'action'}
            ]
          }
        },
        mounted() {
          this.fetchArticles()
        },
        methods: {
          fetchArticles() {
            const token = sessionStorage.getItem('token')
            const URL = 'https://hidden-depths-47488.herokuapp.com/api/article'
            this.$axios({
              method: 'get',
              url: URL,
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
              }
            })
              .then(res => {
                this.listData = res.data.data
              })
              .catch(err => {
                // eslint-disable-next-line
                console.log(err)
              })
          },
          /**
           * used to delete Article
           * @return {[type]} [description]
           */
          deleteArticle(id) {
            const token = sessionStorage.getItem('token')
            const URL = `https://hidden-depths-47488.herokuapp.com/api/article/${id}`
            this.$axios({
              method: 'delete',
              url: URL,
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
              }
            })
              .then(_ => {
                this.fetchArticles()
              })
              .catch(err => {
                // eslint-disable-next-line
                console.log(err)
              })
          }
        }
    }
</script>

<style scoped>

</style>
