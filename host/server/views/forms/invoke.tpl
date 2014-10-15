<form method="POST" action="/packages/invoke/{{package}}/{{service}}">
    <p>Invoke <b></b>{{package}}/{{service}}</p>
    % for field in fields:
    <input name="field"/>
    % end
    <input type="submit" value="Run"/>
</form>