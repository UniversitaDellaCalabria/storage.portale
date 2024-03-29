Vue.options.delimiters = ['[[', ']]'];

Vue.filter('truncate', function (value, length) {
  if (!value) return ''
  value = value.toString()
  if(value.length > length){
    return value.substring(0, length) + "..."
  }else{
    return value
  }
})

Vue.filter('formatDate', function(value) {
  if (value) {
    dt = new Date(value)
    const offsetMs = dt.getTimezoneOffset() * 60 * 1000;
    const dateLocal = new Date(dt.getTime() - offsetMs);
    const str = dateLocal.toISOString().slice(0, 19).replace(/-/g, "/").replace("T", " ");
    return str.slice(0,-3)
  }
});

Vue.filter('val_replace', function (value, value1, value2) {
  if (!value1) return ''
  return value.replace(value1, value2)
})

Vue.filter('capitalize', function (value) {
    if (!value) return ''
    new_value = value.toString()
    return new_value.charAt(0).toUpperCase() + new_value.slice(1)
})
