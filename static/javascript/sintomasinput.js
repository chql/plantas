$(function(){
    var sintomasTags = {};
    var $sintomasInput = $('#sintomas-tags');
    var $sintomasSelect = $('#id_sintomas');

    $('#sintomas-hidden').hide();

    var getSintomaModel = function(tagText, done) {
        $.ajax({
            method: 'PUT',
            url: '/sintomas?q=' + tagText,
            success: done
        });
    };

    var syncing = true;

    $sintomasInput.tagsInput({
        defaultText: 'Adicionar',
        width: '100%',
        onAddTag: function(tagText) {
            if(syncing) return;
            getSintomaModel(tagText, function(response) {
                if(sintomasTags[response.id] === undefined) {
                    var $tagOption = $('<option>');
                    $tagOption.text(response.descricao);
                    $tagOption.prop('selected', true);
                    $tagOption.attr('value', response.id);
                    $tagOption.appendTo($sintomasSelect);
                    sintomasTags[response.id] = $tagOption;
                }
                else {
                    sintomasTags[response.id].prop('selected', true);
                }
            });
        },
        onRemoveTag: function(tagText) {
            getSintomaModel(tagText, function (response) {
                sintomasTags[response.id].prop('selected', false);
            });
        }
    });

    $sintomasSelect.children('option').each(function() {
        sintomasTags[parseInt(this.value)] = $(this);
        if(this.selected)
            $sintomasInput.addTag(this.innerText);
    });

    syncing = false;
});
