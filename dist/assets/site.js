(function(){
  var root=document.documentElement;
  function setLang(l){
    root.lang=l;
    try{localStorage.setItem('fpa-lang',l)}catch(e){}
    document.querySelectorAll('.langs button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.lang===l)});
    var t=document.querySelector('meta[name="title-'+l+'"]'); if(t) document.title=t.content;
  }
  var saved=null; try{saved=localStorage.getItem('fpa-lang')}catch(e){}
  var q=new URLSearchParams(location.search).get('lang');
  setLang(q||saved||'en');
  document.querySelectorAll('.langs button').forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.lang)})});
  var mb=document.querySelector('.menu-btn'),nav=document.querySelector('nav.main');
  if(mb) mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
})();
