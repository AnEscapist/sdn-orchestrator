<template>
    <div>
    <sidebar-menu :menu="menu" />
    </div>
</template>

<script>
    import { SidebarMenu } from 'vue-sidebar-menu'
    export default {
        name: "Sidebar",
        components:{
            SidebarMenu
        },
        data() {
            return {
                menu: [
                    {
                        header: true,
                        title: 'Main Navigation',
                        visibleOnCollapse: true,
                        class: '',
                        attributes: {}
                    },
                    {
                        href: '/',
                        title: 'Dashboard',
                        // icon: 'fa fa-user',
                        /*
                        // custom icon
                        icon: {
                            element: 'span',
                            class: 'fa fa-user',
                            attributes: {}
                            text: ''
                        }
                        */
                        // disabled: true
                        // class: ''
                        // attributes: {}
                        // alias: '/path'
                        /*
                        badge: {
                            text: 'new',
                            class: 'default-badge'
                            // attributes: {}
                            // element: 'span'
                        }
                        */
                    },
                    {
                        title: 'Charts',
                        // icon: 'fa fa-chart-area',
                        child: [
                            {
                                href: '/charts/sublink',
                                title: 'Sub Link',
                            }
                        ]
                    }
                ]
            }
        }
    }
</script>

<style scoped>

</style>
