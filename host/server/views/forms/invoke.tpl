<form method="POST" action="/services/invoke/{{image}}/{{service}}">
    <p>Invoke <b></b>{{image}}/{{service}}</p>
    % for field in fields:
    <input name="field"/>
    % end
    <input type="submit" value="Run"/>
</form>