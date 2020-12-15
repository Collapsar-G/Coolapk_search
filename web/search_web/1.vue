<template>
    <div>
        <v-row justify="center">
            <v-col cols="4" offset="1" align-self="center">
                <v-image-input
                        v-model="imageData"
                        :image-quality="0.85"
                        clearable
                        image-format="jpeg"
                />
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col cols="4">
                <v-btn
                        block
                        rounded
                        color="primary"
                        @click="searchStars"
                        :disabled="loading"
                        :loading="loading"
                >
                    <v-icon left> mdi-magnify</v-icon>
                    Search
                </v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="4" lg="4" sm="6" v-for="(star, i) in resultImages" :key="i">
                <v-card class="mx-auto" max-width="300">
                    <v-img class="white--text align-end" height="300px" :src="star.src">
                        <v-card-title>Top {{ i + 1 }}</v-card-title>
                    </v-img>

                    <v-card-title class="title">
                        {{ star.name }}
                    </v-card-title>
                    <v-card-subtitle class="pb-0">
                        相似度:{{ star.score }}
                    </v-card-subtitle>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    import VImageInput from "vuetify-image-input";

    export default {
        name: "Search",
        components: {
            [VImageInput.name]: VImageInput,
        },
        data: () => ({
            imageData: "",
            loading: false,
            resultImages: [],
            test: "",
        }),
        methods: {
            searchStars() {
                let that = this;
                console.log(this.imageData);
                this.loading = true;
                let params = new FormData();
                params.append("imageData", this.imageData);
                this.axios
                    .post("http://localhost:5000/search", params)
                    .then((response) => {
                        that.test = response.data.stars;
                        that.loading = false;
                        that.resultImages = response.data.stars;
                    })
                    .catch((response) => {
                        console.log(response);
                        that.loading = false;
                    });
            },
        },
    };
</script>

<style scoped></style>
