function init()
{
	//$.getJSON('/hunchworks/skills', handleSkills);
	$("#relatedSkills").tokenInput("/hunchworks/skills");
	$("#id_languages").tokenInput("/hunchworks/languages");
	$("#id_tags").tokenInput("/hunchworks/tags", { theme: 'facebook'});
}

function handleSkills(data)
{
	//alert( data['1'] )
	
}

$(document).ready(init);