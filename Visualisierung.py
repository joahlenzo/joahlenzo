
def pie_chart(value_data, key_data):
    fig = px.pie(values=value_data, names=key_data, title="Anteil Getränke in mL",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    div_pie = plot(fig, output_type="div")
    return div_pie