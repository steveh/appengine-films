lines = File.open("C:/Users/Steve/Downloads/list.htm")

movies = []

for line in lines
  if line =~ /.*tt([0-9]{7,7})\/">(.*)<\/a> \(([0-9]{4,4})\).*">(.*)<\/a.*/
  	movies << {
  		:imdb_id => $1.to_i,
  		:title => $2,
  		:year => $3.to_i,
  		:status => $4
  	}
  end
end

puts movies.to_yaml