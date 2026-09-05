with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add imports
imports_to_add = """import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.staggeredgrid.LazyVerticalStaggeredGrid
import androidx.compose.foundation.lazy.staggeredgrid.StaggeredGridCells
import androidx.compose.foundation.lazy.staggeredgrid.items"""

content = content.replace("import androidx.compose.foundation.lazy.LazyColumn", imports_to_add)

# Replace LazyColumn with LazyVerticalStaggeredGrid
old_list = """                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {"""

new_grid = """                LazyVerticalStaggeredGrid(
                    columns = StaggeredGridCells.Adaptive(minSize = 160.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalItemSpacing = 16.dp,
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {"""

content = content.replace(old_list, new_grid)

# Adjust the card internals to be better suited for narrower columns
old_card_internals = """                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            "Order #${order.orderId}",
                                            fontWeight = FontWeight.ExtraBold,
                                            color = Color(0xFF03045E),
                                            fontSize = 18.sp
                                        )
                                        Text(
                                            "PKR ${order.totalAmount ?: "0"}",
                                            color = Color(0xFF00B4D8),
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 18.sp
                                        )
                                    }"""

new_card_internals = """                                    Column(
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Text(
                                            "Order #${order.orderId}",
                                            fontWeight = FontWeight.ExtraBold,
                                            color = Color(0xFF03045E),
                                            fontSize = 16.sp
                                        )
                                        Text(
                                            "PKR ${order.totalAmount ?: "0"}",
                                            color = Color(0xFF00B4D8),
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 16.sp
                                        )
                                    }"""

content = content.replace(old_card_internals, new_card_internals)

# Remove IntrinsicSize.Min from Row to allow Staggered height to naturally size
old_row = "Row(modifier = Modifier.fillMaxWidth().height(IntrinsicSize.Min)) {"
new_row = "Row(modifier = Modifier.fillMaxWidth()) {"
content = content.replace(old_row, new_row)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
