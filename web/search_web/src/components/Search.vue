<template>
    <v-container>
        <v-row class="text-center">

            <v-col align-self="center" cols="" offset="1">
                <v-text-field width="1000" label="Solo" placeholder="输入关键词搜索，点击app图标下载" solo v-model="value">

                </v-text-field>

            <v-btn :disabled="leading" :loading="leading" @click="clc" elevation="4" outlined raised rounded
                       value="Search">Search
                </v-btn>

            </v-col>
        </v-row>
        <v-row>

            <v-col v-for="(apk, i) in list" :key="i">
                <v-card col="2" class="mx-auto" width="500" height="280"  :href="apk.skipurl">
                    <v-card-text>
                        <v-row>
                            <v-col>
                        <p class="display-1 text--primary">
                            {{apk.name}}
                        </p>
                        <p><a>版本号：{{apk.version}}{{" "}} </a>   <a> |</a>  <a> {{" "}}  {{apk.downloadcount}}</a></p>
                        <p>语言：{{apk.language}} {{" "}}|{{" "}}评分：{{apk.score}} </p></v-col>
                        <v-col>
                        <a :href="apk.downloadurl">
                            <v-img  height="120px" width="120px" :src="apk.imgurl">

                            </v-img>
                        </a>
                            </v-col>
                        </v-row>
                        <div class="text--primary">
                            {{apk.review}}
                        </div>
                    </v-card-text>



                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "Search",
        data: () => ({
            value: "",
            leading: false,
            list: [],

            test: "",
            ecosystem: [
                {
                    text: 'vuetify-loader',
                    href: 'https://github.com/vuetifyjs/vuetify-loader',
                },
                {
                    text: 'github',
                    href: 'https://github.com/vuetifyjs/vuetify',
                },
                {
                    text: 'awesome-vuetify',
                    href: 'https://github.com/vuetifyjs/awesome-vuetify',
                },
            ],
            importantLinks: [
                {
                    text: 'Documentation',
                    href: 'https://vuetifyjs.com',
                },
                {
                    text: 'Chat',
                    href: 'https://community.vuetifyjs.com',
                },
                {
                    text: 'Made with Vuetify',
                    href: 'https://madewithvuejs.com/vuetify',
                },
                {
                    text: 'Twitter',
                    href: 'https://twitter.com/vuetifyjs',
                },
                {
                    text: 'Articles',
                    href: 'https://medium.com/vuetify',
                },
            ],
            whatsNext: [
                {
                    text: 'Explore components',
                    href: 'https://vuetifyjs.com/components/api-explorer',
                },
                {
                    text: 'Select a layout',
                    href: 'https://vuetifyjs.com/getting-started/pre-made-layouts',
                },
                {
                    text: 'Frequently Asked Questions',
                    href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
                },
            ],
        }), methods: {
            clc() {
                let that = this
                this.loading = true
                // let params = new FormData()
                // params.append('imageData', this.imageData)
                this.axios.get('http://localhost:8090/search/' + that.value).then((response) => {
                    console.log(response.data)
                    that.test = response.data
                    that.loading = false
                    that.list = response.data
                }).catch((response) => {
                    console.log("fail", response);
                    that.loading = false
                })
            }
        }
    }
</script>
<style>
    .v-card--reveal {
        bottom: 0;
        opacity: 1 !important;
        position: absolute;
        width: 100%;
    }
</style>
