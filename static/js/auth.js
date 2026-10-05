

const JobSphereAuth = {

    getAccessToken: function () {

        return localStorage.getItem(
            "access_token"
        );
    },


    getRefreshToken: function () {

        return localStorage.getItem(
            "refresh_token"
        );
    },


    setTokens: function (access, refresh) {

        localStorage.setItem(
            "access_token",
            access
        );

        if (refresh) {

            localStorage.setItem(
                "refresh_token",
                refresh
            );
        }
    },


    clearTokens: function () {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "refresh_token"
        );
    },


    isLoggedIn: function () {

        return Boolean(
            this.getAccessToken()
        );
    },


    refreshAccessToken: async function () {

        const refreshToken =
            this.getRefreshToken();

        if (!refreshToken) {

            return false;
        }


        try {

            const response =
                await fetch(
                    "/api/token/refresh/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            refresh:
                                refreshToken
                        })
                    }
                );


            if (!response.ok) {

                this.clearTokens();

                return false;
            }


            const data =
                await response.json();


            this.setTokens(
                data.access,
                data.refresh || refreshToken
            );


            return true;

        } catch (error) {

            console.error(
                "Token refresh failed:",
                error
            );

            this.clearTokens();

            return false;
        }
    },


    fetch: async function (
        url,
        options = {},
        retry = true
    ) {

        const accessToken =
            this.getAccessToken();


        options.headers =
            options.headers || {};


        if (accessToken) {

            options.headers.Authorization =
                `Bearer ${accessToken}`;
        }


        let response;


        try {

            response =
                await fetch(
                    url,
                    options
                );

        } catch (error) {

            throw error;
        }


        /*
         * Access token expired.
         */
        if (
            response.status === 401 &&
            retry
        ) {

            const refreshed =
                await this.refreshAccessToken();


            if (refreshed) {

                return this.fetch(
                    url,
                    options,
                    false
                );
            }


            this.clearTokens();

            window.location.href =
                "/login/";

            return response;
        }


        return response;
    },


    logout: function () {

        this.clearTokens();

        window.location.href =
            "/login/";
    }

};