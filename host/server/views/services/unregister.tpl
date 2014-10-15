% rebase('base.tpl', title='Unregister')

<form method="POST" action="/services/{{service}}/unregister">
    <div>Are you sure you want to unregister <b>{{service}}</b>?</div>
    <div><input type="submit" value="Confirm"/></div>
</form>