
class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
    }

  // Получение CSRF-токена из HTML
  getCsrfToken () {
    return document.getElementsByName('csrfmiddlewaretoken')[0].value;
  }

  getPurchases () {
    return fetch(`/purchases`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addPurchases (id) {
    return fetch(`/add-recipe/${id}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCsrfToken(),
      },
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removePurchases (id){
    return fetch(`/remove-recipe/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCsrfToken(),
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(`/follow/subscribe/${id}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCsrfToken(),
      },
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(`/follow/unsubscribe/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCsrfToken(),
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(`/add-favorites/${id}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'X-CSRFToken': this.getCsrfToken(),
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({
        id: id
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(`/remove-favorites/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCsrfToken(),
      }
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(`/ingredients?query=${text}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
