new Vue({
  el: '#image_app',
  data: {
    searchQuery: '',
    startDate: '',
    endDate: '',
    images: [],
    currentEnlargedImage: null,
    currentPage: 1,
    itemsPerPage: 9,
  },
  created() {
    this.fetchImageData();
  },
  computed: {
    filteredImages() {
      let filteredImages = this.images;
      if (this.searchQuery) {
        filteredImages = filteredImages.filter(image => image.description.includes(this.searchQuery));
      }
      if (this.startDate && this.endDate) {
        const start = new Date(this.startDate);
        const end = new Date(this.endDate);
        filteredImages = filteredImages.filter(image => {
          const createdAt = new Date(image.time_create);
          return createdAt >= start && createdAt <= end;
        });
      }
      return filteredImages;
    },
    paginatedFilteredImages() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredImages.slice(startIndex, endIndex);
    },
    pageCount() {
      return Math.ceil(this.filteredImages.length / this.itemsPerPage);
    },
  },
    created() {
        this.fetchImageData();
  },
  mounted() {
    this.fetchImageData();
  },
  methods: {
    fetchImageData() {
      const vm = this;
      axios.get(`/api/images/`)
        .then(function(response) {
          vm.images = response.data;
          this.pageInfo = response.data;

        })
        .catch(function(error) {
          console.error('Error fetching image data:', error);
        });
    },
    filterImages() {
      const filteredImages = this.filteredImages;
      this.images = filteredImages;
    },
    enlargeImage(index) {
      if (this.currentEnlargedImage !== null) {
        this.currentEnlargedImage = null;
      } else {
        this.currentEnlargedImage = index;
      }
    },
    closeEnlargedImages() {
      this.currentEnlargedImage = null;
    },
    removeQuotes(value) {
      return value.replace(/['"]+/g, '');
    },
    getCircleStyle(item) {
      const color = this.removeQuotes(item.trim().slice(1, -1));
      return {
        background: color
      };
    },
    getImageUrl(path) {
      return path;
    },
    goToPage(page) {
      this.currentPage = page;
    },
  }
});

